from django.shortcuts import get_object_or_404
from jsonschema import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from drf_spectacular.utils import extend_schema
from chat.serializers.conversation_analysis import ConversationTitleGenRequestSerializer
from chat.serializers.chat import ConversationSerializer
from chat.services.model import ConversationTitleService
from core.models.conversation import Conversation
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response
from rest_framework.permissions import IsAuthenticated


class ConversationTitleView(APIView):
    permission_classes = [IsAuthenticated]  

    @extend_schema(
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
        summary="Regenerate conversation title",
        description="Regenerate the title/tag for a specific conversation."
    )
    @transaction.atomic
    def patch(self, request,conversation_id):
        try:     
           

            conversation = get_object_or_404(Conversation, id=conversation_id)
            service = ConversationTitleService()  
            conversation = service.regenerate_conversation_title(
                conversation_id=conversation_id,
                user=request.user
            )           

            return api_response(
                success=True,
                info="CONVERSATION_TAG_REGENERATED_SUCCESSFULLY",
                data={
                    "title_en": conversation.title_en,
                    "title_ar": conversation.title_ar
                },
                status_code=status.HTTP_200_OK
            )

        except ValidationError as e:
            exception_log(e, __file__)
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
                info="REGENERATION_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
