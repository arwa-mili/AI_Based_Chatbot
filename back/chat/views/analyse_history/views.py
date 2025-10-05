from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from chat.serializers.conversation_analysis import ConversationAnalysisSerializer
from core.models.conversation_analysis import ConversationAnalysis

class AnalysisHistoryView(APIView):
    """Get user's analysis history"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["profile"],
        responses={
            200: ConversationAnalysisSerializer(many=True),
            401: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "error": {"type": "string"}
                }
            }
        },
        summary="Get user's analysis history",
        description="Retrieve all analyses for the authenticated user"
    )
    def get(self, request):
        analyses = ConversationAnalysis.objects.filter(user=request.user)
        serializer = ConversationAnalysisSerializer(
            analyses,
            many=True,
            context={'request': request}
        )
        return Response({
            'success': True,
            "data": {'count': analyses.count(),
            'results': serializer.data
            }
        }, status=status.HTTP_200_OK)
