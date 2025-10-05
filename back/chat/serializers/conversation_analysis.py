from rest_framework import serializers
from core.models.conversation import Conversation
from core.models.conversation_analysis import ConversationAnalysis

class AnalyzeConversationsRequestSerializer(serializers.Serializer):
    """Serializer for analysis request using existing conversations"""
    conversation_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="List of conversation IDs to analyze"
    )
    output_lang = serializers.ChoiceField(
        choices=['en', 'ar'],
        default='en',
        help_text="Output language"
    )


class AnalyzeTextRequestSerializer(serializers.Serializer):
    """Serializer for analyzing raw text (without saving to conversations)"""
    chat_histories = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of chat conversations in text format"
    )
    output_lang = serializers.ChoiceField(
        choices=['en', 'ar'],
        default='en'
    )

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    conversation_count = serializers.SerializerMethodField()

    class Meta:
        model = ConversationAnalysis
        fields = [
            'id', 'created_at', 'output_lang', 'summary',
            'detected_language', 'question_count', 'avg_msg_length',
            'common_topics', 'total_conversations', 'total_interactions',
            'status', 'conversation_count'
        ]

    @extend_schema_field(serializers.CharField())
    def get_summary(self, obj) -> str:
        request = self.context.get('request')
        lang = request.GET.get('language_code', 'en') if request else 'en'
        return obj.get_summary(lang)

    @extend_schema_field(serializers.IntegerField())
    def get_conversation_count(self, obj) -> int:
        return obj.conversations.count()
    
class ConversationTitleGenRequestSerializer(serializers.Serializer):
    """Serializer for generating or regenerating conversation title"""
    conversation_id = serializers.IntegerField(
        help_text="ID of the conversation to generate title for"
    )