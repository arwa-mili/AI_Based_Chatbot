from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from chat.services.user_summary_service import UserSummaryService


class UserSummaryView(APIView):
    """Get user's last analysis summary or trigger summarization if quota reached."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve the latest summary of the user's analyses. If the user has reached their quota, a new summary will be generated.",
        tags=["profile"],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "summary": {"type": "string"},
                    "last_updated": {"type": "string"},
                    "language": {"type": "string"},
                    "triggered": {"type": "boolean"}
                }
            }
        }
    )
    def get(self, request):
        user = request.user
        lang = request.GET.get('language_code', 'en')

        service = UserSummaryService()
        result = service.get_user_summary(user, lang)

        return Response(result, status=status.HTTP_200_OK)
