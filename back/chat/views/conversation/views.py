from jsonschema import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from drf_spectacular.utils import extend_schema
from chat.services.chat_crud import ConversationService
from chat.serializers.chat import ConversationSerializer, CreateConversationSerializer, GetConversationsReq, GetConversationsSerializer
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response
import os
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]  


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

        
        
        
        
        