from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=["google", "facebook", "apple"])
    token = serializers.CharField()  
    nonce = serializers.CharField(required=False, allow_blank=True)