from typing import List, Dict
import re
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from django.utils import timezone
from core.models.conversation import Conversation
from core.models.conversation_line import ConversationLine
from core.models.conversation_analysis import ConversationAnalysis
from core.models.user import User
from core.enums.enums import SentByEnum

class ModelManager:
    """Singleton for ML models."""
    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not ModelManager._loaded:
            self._load_models()
            ModelManager._loaded = True

    def _load_models(self):
        # English summarization (BART)
        self.summarizer_en = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        # Arabic summarization (mT5)
        self.tokenizer_ar = AutoTokenizer.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")
        self.model_ar = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")
        if torch.cuda.is_available():
            self.model_ar = self.model_ar.cuda()


class ConversationExtractor:
    """Extract conversation texts in the requested language."""

    @staticmethod
    def extract(conversation_ids: List[int], user: User, lang_code: str) -> List[str]:
        conversations = Conversation.objects.filter(id__in=conversation_ids, user=user).prefetch_related('lines')
        chat_texts = []

        for conv in conversations:
            lines = conv.lines.order_by('created_at')
            chat_lines = []

            for line in lines:
                # Dynamically get text based on requested language
                text = line.get_text(lang_code)
                prefix = "User:" if line.sent_by == SentByEnum.USER.value else "Bot:"
                if lang_code == 'ar':
                    prefix = "المستخدم:" if line.sent_by == SentByEnum.USER.value else "بوت:"
                chat_lines.append(f"{prefix} {text}")

            if chat_lines:
                chat_texts.append("\n".join(chat_lines))
        return chat_texts


class ChatAnalyzerService:
    """Analyze conversations and produce plain-text summaries."""

    def __init__(self):
        self.model_manager = ModelManager()
        self.extractor = ConversationExtractor()

    def analyze_conversations(
        self, conversation_ids: List[int], user: User, output_lang: str = 'en'
    ) -> ConversationAnalysis:
        analysis = ConversationAnalysis.objects.create(
            user=user, output_lang=output_lang, status='processing'
        )
        try:
            chat_texts = self.extractor.extract(conversation_ids, user, output_lang)
            if not chat_texts:
                raise ValueError("No valid conversations found.")
            # Link conversations
            analysis.conversations.set(Conversation.objects.filter(id__in=conversation_ids, user=user))
            # Perform analysis
            result = self._perform_analysis(chat_texts, output_lang)
            # Save results
            self._save_results(analysis, result, output_lang)
            # Update user
            self._update_user(user, result, output_lang)
            analysis.status = 'completed'
            analysis.save()
            return analysis
        except Exception as e:
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.save()
            raise

    def analyze_text(
        self, messages: List[str], user: User, output_lang: str = 'en'
    ) -> Dict:
        """Analyze raw user messages without saving conversations."""
        analysis = ConversationAnalysis.objects.create(
            user=user, output_lang=output_lang, status='processing'
        )
        try:
            result = self._perform_analysis(messages, output_lang)
            self._save_results(analysis, result, output_lang)
            self._update_user(user, result, output_lang)
            analysis.status = 'completed'
            analysis.save()
            return {"success": True, "analysis_id": str(analysis.id), "summary": result['summary']}
        except Exception as e:
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.save()
            raise

    def _perform_analysis(self, chat_texts: List[str], lang_code: str) -> Dict:
        """Core analysis logic."""
        user_messages = []
        bot_messages = []

        for chat in chat_texts:
            for line in chat.split('\n'):
                if line.startswith('User:') or line.startswith('المستخدم:'):
                    user_messages.append(re.sub(r'^(User:|المستخدم:)', '', line).strip())
                elif line.startswith('Bot:') or line.startswith('بوت:'):
                    bot_messages.append(re.sub(r'^(Bot:|بوت:)', '', line).strip())

        summary = self._generate_summary(user_messages, lang_code)

        return {
            "summary": summary,
            "total_conversations": len(chat_texts),
            "total_interactions": len(user_messages),
            "total_user_messages": len(user_messages),
            "total_bot_messages": len(bot_messages)
        }

    def _generate_summary(self, messages: List[str], lang_code: str) -> str:
        """Generate a human-friendly, plain-text summary."""
        if not messages:
            return "No user interactions to summarize."

        text_to_summarize = ' '.join(messages)[:1024]  

        if lang_code == 'ar':
            input_text = f"لخص المحتوى التالي بطريقة مبسطة ومفهومة للمستخدم: {text_to_summarize}"
            try:
                input_ids = self.model_manager.tokenizer_ar.encode(
                    input_text, return_tensors="pt", max_length=512, truncation=True
                )
                if torch.cuda.is_available():
                    input_ids = input_ids.cuda()
                output_ids = self.model_manager.model_ar.generate(
                    input_ids, max_length=150, min_length=40, num_beams=4
                )
                summary = self.model_manager.tokenizer_ar.decode(output_ids[0], skip_special_tokens=True)
            except:
                summary = "المستخدم تحدث عن مواضيع متعددة."
        else:
            try:
                result = self.model_manager.summarizer_en(
                    text_to_summarize, max_length=150, min_length=50, do_sample=False
                )
                summary = result[0]['summary_text']
            except:
                summary = "The user spoke about several topics."

        summary = re.sub(r'\s+', ' ', summary).strip()
        return summary

    def _save_results(self, analysis: ConversationAnalysis, result: Dict, lang_code: str):
        if lang_code == 'ar':
            analysis.summary_ar = result['summary']
        else:
            analysis.summary_en = result['summary']

        analysis.total_conversations = result['total_conversations']
        analysis.total_interactions = result['total_interactions']
        analysis.total_user_messages = result['total_user_messages']
        analysis.total_bot_messages = result['total_bot_messages']
        analysis.save()

    def _update_user(self, user: User, result: Dict, lang_code: str):
        if lang_code == 'ar':
            user.last_analysis_summary_ar = result['summary']
        else:
            user.last_analysis_summary_en = result['summary']
        user.last_analysis_date = timezone.now()
        user.save(update_fields=['last_analysis_summary_en', 'last_analysis_summary_ar', 'last_analysis_date'])
