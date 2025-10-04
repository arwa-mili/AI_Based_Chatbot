from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.db import transaction
from django.utils import timezone
from core.utils.logger import exception_log
from core.models import Language, User
from auth.serializers.register import RegisterSerializer
from auth.services.user_service import UserService

from core.utils.response_wrapper import api_response
            
class RegisterView(APIView):
    authentication_classes = []

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: {
                "description": "Registration successful",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"}
                }
            },
            400: {
                "description": "Registration failed",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"}
                }
            }
        },
        summary="Register a new user",
        description="Creates a new user account, accepting its email, password , name and prefered language"
    )
    @transaction.atomic
    def post(self, request):
        try:
            language_code = request.headers.get("language_code", "en")  
            if request.data.get("password") != request.data.get("confirmPassword"):
                return api_response(
                    success=False,
                    info="PASSWORDS_NENTERED_DO_NOT_MATCH",
                    error="Passwords do not match, please check then twice",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            email = request.data.get("email")
            if email and User.objects.filter(email=email).only('id').exists():
                return api_response(
                    success=False,
                    info="EMAIL_ALREADY_EXISTS",
                    error="User with this email already exists",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
        
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data


            language = Language.objects.filter(language_code=language_code).only('id').first() if language_code else None
            
            if (language == None):
                return api_response(
                    success=False,
                    info="LANGUAGE_NOT_SUPPORTED",
                    error="The language you requested is not supported yet by our system",
                    status_code=status.HTTP_409_CONFLICT
                )

            user_data = {
                **validated_data,
                "language_code": language_code
            }
            user_data.pop("confirmPassword","")

            user = UserService.create_user(**user_data)
                        
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token  
            

            return api_response(
                success=True,
                info="REGISTRATION_SUCCESSFUL",
                data={
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "name": user.name,
                        "language_code": user.language_code
                    },
                    "accessToken": str(access),
                    "refreshToken": str(refresh)
                },
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            exception_log(e,__file__)
            transaction.set_rollback(True)
            return api_response(
                success=False,
                info="VALIDATION_ERROR",
                error=str(e.detail),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="REGISTRATION_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
