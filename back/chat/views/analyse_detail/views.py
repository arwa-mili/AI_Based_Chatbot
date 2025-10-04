from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import torch

from chat.serializers.conversation_analysis import AnalyzeConversationsRequestSerializer, ConversationAnalysisSerializer
from chat.services.model import ChatAnalyzerService, ModelManager
from drf_spectacular.utils import extend_schema

from chat.serializers.conversation_analysis import ConversationAnalysisSerializer
from core.models.conversation_analysis import ConversationAnalysis

class AnalysisDetailView(APIView):
    """Get specific analysis details"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: ConversationAnalysisSerializer,
            404: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "error": {"type": "string"}
                }
            }
        },
        summary="Get specific analysis",
        description="Retrieve a single analysis by its ID for the authenticated user"
    )
    def get(self, request, analysis_id):
        analysis = get_object_or_404(
            ConversationAnalysis,
            id=analysis_id,
            user=request.user
        )
        serializer = ConversationAnalysisSerializer(
            analysis,
            context={'request': request}
        )
        return Response({
            'success': True,
            'analysis': serializer.data
        }, status=status.HTTP_200_OK)
