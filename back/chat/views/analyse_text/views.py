from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chat.serializers.conversation_analysis import AnalyzeTextRequestSerializer
from chat.services.model import ChatAnalyzerService
from drf_spectacular.utils import extend_schema


class AnalyzeTextView(APIView):
    """Analyze raw text conversations"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AnalyzeTextRequestSerializer,
        responses={200: AnalyzeTextRequestSerializer} 
    )
    def post(self, request):
        serializer = AnalyzeTextRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ChatAnalyzerService()
            result = service.analyze_text(
                chat_histories=serializer.validated_data['chat_histories'],
                user=request.user,
                output_lang=serializer.validated_data['output_lang']
            )
            
            return Response({
                'success': True,
                'result': result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
