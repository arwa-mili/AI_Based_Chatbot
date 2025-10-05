from rest_framework import serializers
from core.models import User

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "created_at",
            "last_login"
        ]
        read_only_fields = fields

        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "email"
        ]
