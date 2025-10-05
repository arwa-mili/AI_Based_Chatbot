from django.db.models import F 
from rest_framework.views import APIView
from rest_framework import status
from langdetect import detect
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.db import transaction
from django.utils.html import escape, linebreaks

from chat.services.chat_crud import ConversationService
from chat.services.model import ConversationTitleService
from core.models import Conversation, ConversationLine, Language
from core.enums.enums import ModelUsedEnum, SentByEnum
from chat.serializers.chat import ChatRequestSerializer, ConversationSerializer
from core.utils.response_wrapper import api_response
import os

from google import genai
import openai
from openai import OpenAI

from core.utils.translate_text import translate_text


# ---------------------------
# AI Client Factory
# ---------------------------
def get_ai_client(provider: str):
    """
    Return the client for the requested AI provider.
    """
    if provider == ModelUsedEnum.GEMINI:
        api_key = 'AIzaSyAU6oQbS23u_hXPLAqZIwzOpFlDvRikBEs'
        return genai.Client(api_key=api_key)
    # view at https://openrouter.ai/deepseek/deepseek-chat-v3.1:free/api
    #view at https://openrouter.ai/openai/gpt-oss-20b:free

    elif (provider == ModelUsedEnum.DEEPSEEK or provider == ModelUsedEnum.GPT):
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        )
    else:
        raise ValueError(f"Unknown AI provider: {provider}")


# ---------------------------
# ChatView: Main AI interaction
# ---------------------------
class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChatRequestSerializer,
        parameters=[
            OpenApiParameter("language_code", OpenApiTypes.STR, description="Language code (e.g., 'en', 'ar')", required=False)
        ],
        responses={
            200: ConversationSerializer,
            400: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                }
            }
        },
        summary="Ask a question to AI chat",
        description="Creates a new conversation if conversation_id is not provided and returns AI response"
    )
    @transaction.atomic
    def post(self, request):
        try:
            question = request.data.get("text")
            if not question:
                return api_response(
                    success=False,
                    info="QUESTION_REQUIRED",
                    error="You must provide a question",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            language_to_be_used = detect(question) 
            if language_to_be_used not in ['en', 'ar']:
                language_to_be_used = 'en'

            conversation_id = request.data.get("conversation_id")
            user = request.user if request.user.is_authenticated else None
            title = request.data.get("title", "New Conversation")
            provider = request.data.get("provider", ModelUsedEnum.GEMINI)
            model_name = request.data.get("model")
            
            
            language_obj = Language.objects.filter(language_code=language_to_be_used).first()
            if not language_obj:
                language_obj = Language.objects.filter(language_code='en').first()


            text_field_name = f"text_{language_to_be_used}"
            text_html_field_name = f"text_html_{language_to_be_used}"
            title_field_name = f"title_{language_to_be_used}"
            text_opposite_language = f"text_{'ar' if language_to_be_used == 'en' else 'en'}"
            

            # Fetch or create conversation
            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id)
            else:
                conversation = Conversation.objects.create(
                    user=user,
                    **{title_field_name: title}
                )
                # Increment conversations_count atomically
                from django.contrib.auth import get_user_model
                User = get_user_model()
                User.objects.filter(id=user.id).update(conversations_count=F('conversations_count') + 1)


            # Build conversation history
            chat_history = [
                (getattr(line, text_field_name, ""), line.sent_by)
                for line in conversation.lines.all()
            ]
            history_text = "\n".join([f"{sent_by}: {text}" for text, sent_by in chat_history if text])
            user_history_text = f"{history_text}\nUser: {question}" if history_text else f"User: {question}"

            system_instruction = """As an AI assistant, answer the user's question using your own knowledge.
Include previous chat history for context but do not invent information.detect user language from the question and respond in the same language.Note that languages supported are English and Arabic only . But you must strictly respond in one single language ! Start directly from yur answer!"""

            client = get_ai_client(provider)

            # --- Generate AI response ---
            if provider == ModelUsedEnum.GEMINI:
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config=genai.types.GenerateContentConfig(system_instruction=system_instruction)
                )
                response = chat.send_message(user_history_text)
                answer = response.text

            elif provider == ModelUsedEnum.DEEPSEEK:

                completion = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3.1:free",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_history_text}
                    ]
                )
                answer = completion.choices[0].message.content
                
            elif provider == ModelUsedEnum.GPT:
                print("heere")
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b:free",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_history_text}
                    ]
                )
                answer = completion.choices[0].message.content

            else:
                raise ValueError(f"Provider {provider} is not supported")

            # --- Convert AI response to plain text + HTML ---
            plain_text = answer.strip()
            html_text = linebreaks(escape(plain_text))  
            opposite_language = 'ar' if language_to_be_used == 'en' else 'en'
            user_text = translate_text(question, language_to_be_used, opposite_language)
            bot_text = translate_text(plain_text, language_to_be_used, opposite_language)


            ConversationLine.objects.create(
                conversation=conversation,
                sent_by=SentByEnum.USER.value,
                model_used=provider,
                language=language_obj,
                **{
                    text_field_name: question, 
                    text_opposite_language: user_text,
                    text_html_field_name: linebreaks(question) 
                }
            )

            # --- Save AI (bot) response ---
            ConversationLine.objects.create(
                conversation=conversation,
                sent_by=SentByEnum.BOT.value,
                model_used=provider,
                language=language_obj,
                **{
                    text_field_name: plain_text,
                    text_opposite_language: bot_text,
                    text_html_field_name: linebreaks(answer.strip()) 
                }
            )
            if (not conversation_id):
                service = ConversationTitleService()  
                conversation = service.regenerate_conversation_title(
                conversation_id=conversation.id,
                user=request.user
            )  
            

            serializer = ConversationSerializer(conversation)
            return api_response(
                success=True,
                info="QUESTION_ANSWERED",
                data={
                    "conversation": serializer.data,
                    "content": html_text
                },
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            transaction.set_rollback(True)
            from core.utils.logger import exception_log
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="CHAT_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


# ---------------------------
# ConversationMessagesView: Fetch conversation lines
# ---------------------------
class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("language_code", OpenApiTypes.STR, description="Language code (e.g., 'en', 'ar')", required=False),
            OpenApiParameter("pageNumber", OpenApiTypes.INT, description="Page number for pagination", required=False),
            OpenApiParameter("pageSize", OpenApiTypes.INT, description="Number of items per page", required=False),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "text": {"type": "string"},
                                        "text_html": {"type": "string"},
                                        "sent_by": {"type": "string", "enum": ["USER", "BOT"]},
                                        "created_at": {"type": "string", "format": "date-time"},
                                        "model_used": {"type": "string"}
                                    }
                                }
                            },
                            "totalPages": {"type": "integer"},
                            "pageNumber": {"type": "integer"},
                            "pageSize": {"type": "integer"},
                        }
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                }
            }
        },
        summary="Get messages of a specific conversation",
        description="Returns paginated messages of a conversation in a specified language, including plain text and HTML versions"
    )
    def get(self, request, conversation_id):
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            pageNumber = int(request.GET.get("pageNumber", 1))
            pageSize = int(request.GET.get("pageSize", 10))
            user = request.user if request.user.is_authenticated else None

            data = ConversationService.get_conversation_messages(
                conversation_id=conversation.id,
                pageNumber=pageNumber,
                pageSize=pageSize,
                user_id=user.id if user else None
            )

            return api_response(
                success=True,
                info="MESSAGES_RETRIEVED",
                data=data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return api_response(
                success=False,
                info="MESSAGES_FETCH_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
