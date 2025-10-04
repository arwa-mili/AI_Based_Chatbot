from rest_framework import serializers
from core.models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "email", 
#             "password", 
#             "name", 
#             "language_code",
#         ]
#         extra_kwargs = {
#             "password": {"write_only": True}
#         }


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    name = serializers.CharField()
