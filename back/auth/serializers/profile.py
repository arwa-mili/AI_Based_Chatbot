from rest_framework import serializers
from core.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source="langauge.language_name", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "language",
            "language_code"
        ]
        read_only_fields = fields

        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "language_code"
        ]
