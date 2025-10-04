from rest_framework import serializers

from core.enums.enums import ModelUsedEnum

class ChatRequestSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    text = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_blank=True)
    provider = serializers.ChoiceField(
        choices=[(tag.value, tag.name) for tag in ModelUsedEnum],
        default=ModelUsedEnum.GEMINI.value,
        required=False
    )
    
class GetConversationsReq(serializers.Serializer):
    pageSize = serializers.IntegerField(required=False, default=20)
    pageNumber = serializers.IntegerField(required=False, default=1)
    search = serializers.CharField(required=False, allow_blank=True)
    
class ConversationLineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text_ar = serializers.CharField()
    text_en = serializers.CharField()
    sent_by = serializers.CharField()
    model_used = ModelUsedEnum
    language_code = serializers.CharField(source='language.language_code', allow_null=True)
    created_at = serializers.DateTimeField()
    
    
class ConversationGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
class GetConversationsSerializer(serializers.Serializer):
    items = ConversationGetSerializer(many=True)  
    pageSize = serializers.IntegerField()
    pageNumber = serializers.IntegerField()
    totalPages = serializers.IntegerField()

class ConversationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title_en = serializers.CharField()
    title_ar = serializers.CharField()

    user_id = serializers.IntegerField(source='user.id', allow_null=True)
    user_name = serializers.CharField(source='user.name', allow_null=True)
    language_code = serializers.CharField(source='language.language_code', allow_null=True)
    lines = ConversationLineSerializer(many=True)
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['lines'] = sorted(ret['lines'], key=lambda x: x['created_at'])
        return ret
    
    
class CreateConversationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user.id', allow_null=False)

    