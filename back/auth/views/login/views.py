from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from auth.serializers.login import LoginSerializer, SocialLoginSerializer
from auth.services.user_service import AccountNotVerifiedError, UserService
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response

class LoginView(APIView):
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                "description": "Login successful",
                "type": "object",
                "properties": {
                    "accessToken": {"type": "string", "description": "JWT access token"},
                    "refreshToken": {"type": "string", "description": "JWT refresh token"},
                },
            },
            400: {
                "description": "Login failed",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                },
            },
            
            403: {
                "description": "User Not Verified",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                },
            },
        },
        summary="Authenticate user and return JWT tokens",
        description="Accepts email and password, returns access and refresh tokens if credentials are correct."
    )
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tokens = UserService.login_user(**serializer.validated_data)
            
            return api_response(
                success=True,
                info="LOGIN_SUCCESSFUL",
                data=tokens,
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="LOGIN_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
