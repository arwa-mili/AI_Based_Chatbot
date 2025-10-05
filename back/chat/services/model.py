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
from collections import Counter


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
        # Model no more used in this context , suitable better for text or pdf summarizing..
        # In conversations it gave nonesense
        # self.summarizer_en = pipeline(
        #     "summarization",
        #     model="facebook/bart-large-cnn",
        #     device=0 if torch.cuda.is_available() else -1
        # )
        # Arabic summarization (mT5)
        self.tokenizer_ar = AutoTokenizer.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")
        self.model_ar = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")
        if torch.cuda.is_available():
            self.model_ar = self.model_ar.cuda()
            
        # Flan-T5 for title generation & conversation summaries (supports both Arabic and English but used in english here)
        self.title_generator_en = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",  # Use flan-t5-large for better quality
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Option 1: AraT5 for Arabic (specialized for Arabic)
        try:
            self.title_tokenizer_ar = AutoTokenizer.from_pretrained("UBC-NLP/AraT5-base-title-generation")
            self.title_model_ar = AutoModelForSeq2SeqLM.from_pretrained("UBC-NLP/AraT5-base-title-generation")
            if torch.cuda.is_available():
                self.title_model_ar = self.title_model_ar.cuda()
            self.arabic_title_method = 'arat5'
        except:
            # Option 2: Fallback to mBART-50 (good multilingual support)
            self.title_tokenizer_ar = AutoTokenizer.from_pretrained("facebook/mbart-large-50")
            self.title_model_ar = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50")
            if torch.cuda.is_available():
                self.title_model_ar = self.title_model_ar.cuda()
            self.arabic_title_method = 'mbart'


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
        """Generate thematic analysis of user interests."""
        if not messages:
            return "No user interactions to summarize." if lang_code == 'en' else "لا توجد محادثات للتحليل."

        # Combine messages with more context
        text_to_analyze = ' '.join(messages)[:800]

        if lang_code == 'ar':
            prompt = f"""قم بتحليل الأسئلة التالية واكتب جملة واحدة فقط توضح المواضيع الرئيسية التي يهتم بها المستخدم:

{text_to_analyze}
 بحثت في الآونة الأخيرة عن:"""
            try:
                input_ids = self.model_manager.tokenizer_ar.encode(
                    prompt, return_tensors="pt", max_length=512, truncation=True
                )
                if torch.cuda.is_available():
                    input_ids = input_ids.cuda()
                    
                output_ids = self.model_manager.model_ar.generate(
                    input_ids,
                    max_length=100,
                    min_length=20,
                    num_beams=5,
                    no_repeat_ngram_size=3,
                    early_stopping=True
                )
                summary = self.model_manager.tokenizer_ar.decode(
                    output_ids[0], skip_special_tokens=True
                ).strip()
                
                # Validate output
                if len(summary) < 10 or self._is_repetitive(summary):
                    summary = self._extract_topics_fallback(messages, 'ar')
                    
            except Exception as e:
                print(f"⚠ Arabic generation error: {e}")
                summary = self._extract_topics_fallback(messages, 'ar')
                
        else:  # English
            prompt = f"""Analyze these user questions and write ONE clear sentence about the main topics the user asks about. Be specific.

User messages: {text_to_analyze}

Analysis: The user asks about"""
            
            try:
                result = self.model_manager.title_generator_en(
                    prompt,
                    max_length=80,
                    min_length=15,
                    num_beams=5,
                    no_repeat_ngram_size=3,
                    early_stopping=True,
                    do_sample=False
                )
                summary = result[0]['generated_text'].strip()
                
                # Clean output
                summary = self._clean_summary_output(summary)
                
                if len(summary) < 10 or self._is_repetitive(summary):
                    summary = self._extract_topics_fallback(messages, 'en')
                else:
                    if not summary.lower().startswith('the user'):
                        summary = f"You searched recently about {summary}"
                    if not summary.endswith('.'):
                        summary += '.'
                        
            except Exception as e:
                print(f"⚠ English generation error: {e}")
                summary = self._extract_topics_fallback(messages, 'en')

        # Final cleanup
        summary = re.sub(r'\s+', ' ', summary).strip()
        return summary

    def _is_repetitive(self, text: str) -> bool:
        """Check if text contains excessive repetition."""
        words = text.lower().split()
        if len(words) < 3:
            return True
        
        # Check for repeated phrases (bigrams)
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        unique_bigrams = set(bigrams)
        
        # If more than 30% duplicates, it's repetitive
        if len(bigrams) > 0 and len(unique_bigrams) / len(bigrams) < 0.7:
            return True
        
        return False

    def _clean_summary_output(self, text: str) -> str:
        """Clean model-generated text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove quotes and leading/trailing punctuation
        text = text.strip('"\'.,;:')
        
        # Remove common model prefixes
        prefixes = [
            'analysis:', 'summary:', 'the user is interested in:',
            'answer:', 'result:', 'output:', 'topics:'
        ]
        text_lower = text.lower()
        for prefix in prefixes:
            if text_lower.startswith(prefix):
                text = text[len(prefix):].strip()
                text_lower = text.lower()
        
        return text

    def _extract_topics_fallback(self, messages: List[str], lang_code: str) -> str:
        """Robust fallback: Extract topics using keyword frequency."""
        
        if lang_code == 'ar':
            stop_words = {
                'في', 'من', 'إلى', 'على', 'أن', 'هذا', 'هذه', 'هو', 'هي', 'ما',
                'هل', 'كان', 'كانت', 'و', 'أو', 'لا', 'نعم', 'عن', 'مع', 'لكن',
                'ذلك', 'التي', 'الذي', 'كل', 'بعض', 'أي', 'كيف', 'متى', 'أين',
                'لماذا', 'ليس', 'قد', 'لقد', 'إذا', 'عندما', 'بين', 'حتى', 'ثم',
                'ماذا', 'يكون', 'تكون', 'كانت', 'يكونوا', 'هناك', 'هنا'
            }
            # Extract Arabic words (2+ chars)
            all_words = []
            for msg in messages:
                words = re.findall(r'[\u0600-\u06FF]{2,}', msg)
                all_words.extend([w for w in words if w not in stop_words])
                
        else:  # English
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'can', 'i', 'you', 'he', 'she', 'it',
                'they', 'we', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
                'his', 'their', 'this', 'that', 'these', 'those', 'what', 'which',
                'who', 'when', 'where', 'why', 'how', 'give', 'please', 'tell',
                'about', 'more', 'explain', 'yes', 'no', 'ok', 'thanks', 'thank',
                'get', 'make', 'know', 'think', 'take', 'see', 'come', 'want'
            }
            # Extract English words (3+ chars)
            all_words = []
            for msg in messages:
                words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                all_words.extend([w for w in words if w not in stop_words])
        
        # Count frequency
        word_freq = Counter(all_words)
        
        # Get top meaningful keywords
        generic_words = {
            'thing', 'things', 'stuff', 'something', 'anything', 'everything',
            'someone', 'anyone', 'everyone', 'somewhere', 'anywhere'
        }
        
        top_topics = []
        for word, count in word_freq.most_common(15):
            if word not in generic_words and len(word) > 2:
                top_topics.append(word)
            if len(top_topics) >= 6:
                break
        
        # Handle no topics found
        if not top_topics:
            return "المستخدم تحدث عن مواضيع عامة." if lang_code == 'ar' else "The user discussed various general topics."
        
        # Construct natural sentence
        if lang_code == 'ar':
            if len(top_topics) == 1:
                topics_str = top_topics[0]
            elif len(top_topics) == 2:
                topics_str = f"{top_topics[0]} و {top_topics[1]}"
            else:
                topics_str = '، '.join(top_topics[:-1]) + f' و {top_topics[-1]}'
            return f"المستخدم يسأل عن مواضيع متعلقة بـ {topics_str}."
        else:
            if len(top_topics) == 1:
                topics_str = top_topics[0]
            elif len(top_topics) == 2:
                topics_str = f"{top_topics[0]} and {top_topics[1]}"
            else:
                topics_str = ', '.join(top_topics[:-1]) + f', and {top_topics[-1]}'
            return f"The user asks about topics related to {topics_str}."

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


class ConversationTitleService:
    """Service to generate conversation subject/title in English and Arabic."""

    def __init__(self):
        self.model_manager = ModelManager()

    def regenerate_conversation_title(self, conversation_id: int, user: User) -> Conversation:
        conversation = Conversation.objects.filter(id=conversation_id, user=user).first()
        if not conversation:
            raise ValueError("Conversation not found")

        last_lines = conversation.lines.order_by('-created_at')[:6]
        if not last_lines:
            raise ValueError("No conversation lines found")

        texts_en = [line.text_en for line in reversed(last_lines)]
        texts_ar = [line.text_ar for line in reversed(last_lines)]

        # Generate titles using appropriate models
        title_en = self._generate_topic_title(texts_en, lang='en')
        title_ar = self._generate_topic_title(texts_ar, lang='ar')

        conversation.title_en = title_en
        conversation.title_ar = title_ar
        conversation.save(update_fields=['title_en', 'title_ar'])

        return conversation

    def _generate_topic_title(self, messages: List[str], lang: str) -> str:
        """Generate a short, topic-style title (English: Flan-T5, Arabic: AraT5/mBART)."""
        if not messages:
            return "No Title" if lang == 'en' else "بدون عنوان"

        text = " ".join(messages)[:500]

        try:
            if lang == 'ar':
                # Use Arabic-specific models (AraT5 or mBART)
                if self.model_manager.arabic_title_method == 'keywords':
                    # Fallback to keyword extraction if models failed to load
                    return self._extract_keywords(text, lang='ar')
                
                tokenizer = self.model_manager.title_tokenizer_ar
                model = self.model_manager.title_model_ar
                
                if self.model_manager.arabic_title_method == 'arat5':
                    # AraT5: Feed text directly without instruction
                    input_ids = tokenizer.encode(
                        text,
                        return_tensors="pt",
                        max_length=512,
                        truncation=True
                    )
                elif self.model_manager.arabic_title_method == 'mbart':
                    # mBART: Set source language
                    tokenizer.src_lang = "ar_AR"
                    input_ids = tokenizer.encode(
                        text,
                        return_tensors="pt",
                        max_length=512,
                        truncation=True
                    )
                
                if torch.cuda.is_available():
                    input_ids = input_ids.cuda()
                
                # Generate title
                output_ids = model.generate(
                    input_ids,
                    max_length=15,
                    min_length=3,
                    num_beams=5,
                    early_stopping=True,
                    no_repeat_ngram_size=2,
                    length_penalty=0.8
                )
                
                title = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
                
                # Check if result is valid
                if not title or len(title.strip()) < 2 or title.isspace():
                    print(f"⚠ Arabic model returned empty/whitespace: '{title}'")
                    return self._extract_keywords(text, lang='ar')
                
            else:
                # English: Use Flan-T5
                prompt = f"Write a short and concise title for this conversation in 3-5 words only: {text}"
                result = self.model_manager.title_generator_en(
                    prompt,
                    max_length=20,
                    min_length=3,
                    do_sample=False,
                    num_beams=5,
                    early_stopping=True
                )
                title = result[0]['generated_text'].strip()
                
                if not title or len(title.strip()) < 2:
                    return self._extract_keywords(text, lang='en')
            
            # Clean up title
            title = re.sub(r'\s+', ' ', title).strip()
            title = title.strip('"\'.,;:')
            
            # Length limit
            if len(title) > 60:
                title = title[:60].rsplit(' ', 1)[0]
            
            # Final validation
            if len(title) < 2:
                return "محادثة" if lang == 'ar' else "Conversation"
            
            return title
            
        except Exception as e:
            print(f"❌ Error generating {lang} title: {e}")
            # Fallback to keyword extraction
            try:
                return self._extract_keywords(text, lang)
            except:
                return "محادثة" if lang == 'ar' else "Conversation"
    
    def _extract_keywords(self, text: str, lang: str) -> str:
        """Extract keywords as fallback title generation."""
        if lang == 'ar':
            stop_words = {
                'في', 'من', 'إلى', 'على', 'أن', 'هذا', 'هذه', 'هو', 'هي', 'ما',
                'هل', 'كان', 'كانت', 'و', 'أو', 'لا', 'نعم', 'عن', 'مع', 'لكن',
                'ذلك', 'التي', 'الذي', 'كل', 'بعض', 'أي', 'كيف', 'متى', 'أين'
            }
            # Extract Arabic words
            words = re.findall(r'[\u0600-\u06FF]+', text)
        else:
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                'for', 'of', 'with', 'is', 'are', 'was', 'were', 'i', 'you',
                'he', 'she', 'it', 'they', 'we', 'this', 'that', 'what', 'how'
            }
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter meaningful words
        keywords = [w for w in words if w.lower() not in stop_words and len(w) > 2]
        
        # Get first 3-4 unique words
        unique_keywords = []
        for word in keywords:
            if word not in unique_keywords:
                unique_keywords.append(word)
            if len(unique_keywords) >= 4:
                break
        
        if unique_keywords:
            title = " ".join(unique_keywords[:4])
            return title[:60]  # Limit length
        else:
            return "محادثة" if lang == 'ar' else "Conversation"