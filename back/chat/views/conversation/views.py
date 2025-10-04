from jsonschema import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema
from chat.services.chat_crud import ConversationService
from core.models import Conversation, ConversationLine, Language
from core.enums.enums import ModelUsedEnum, SentByEnum
from chat.serializers.chat import ChatRequestSerializer, ConversationSerializer, CreateConversationSerializer, GetConversationsReq, GetConversationsSerializer
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response
import os
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]  


    @extend_schema(
        request=CreateConversationSerializer,
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
        summary="Create the conversation",
        description="Creates a new conversation object which will includes the replications"
    )
    @transaction.atomic
    def post(self, request):
        try:
            
            user = request.user if request.user.is_authenticated else None
            main_language = request.GET.get("language_code", "en")
            title_en= ""
            
            title_ar= ""
            
            ConversationService.create_conversation(user.id,title_en, title_ar,main_language)
                

            return api_response(
                success=True,
                info="CONVERSATION_GENERATED_SUCCESSFULLY",
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return api_response(
                success=False,
                info="VALIDATION_ERROR",
                error=str(e.detail),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="REGISTRATION_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        parameters=[
            OpenApiParameter("pageSize", int, description="Number of items per page", required=True),
            OpenApiParameter("pageNumber", int, description="Page number", required=True),
            OpenApiParameter("search", str, description="Search string (optional)", required=False),
        ],
        responses={
            200: GetConversationsSerializer,
            400: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                }
            }
        },
        summary="get conversations",
        description="get conversations"
    )
    @transaction.atomic
    def get(self, request):
        try:
            
            user = request.user if request.user.is_authenticated else None
            language_code = request.GET.get("language_code", "en")


            
            
            convs = ConversationService.get_conversations(1,20, user or 1,language_code)
                

            return api_response(
                success=True,
                info="CONVERSATION_GENERATED_SUCCESSFULLY",
                data=convs,
                status_code=status.HTTP_200_OK
            )
        except ValidationError as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return api_response(
                success=False,
                info="VALIDATION_ERROR",
                error=str(e.detail),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="PROBLEM",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        
        
        
        
        