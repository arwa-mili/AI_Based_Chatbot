from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema
from django.db import transaction
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response
from auth.services.user_service import UserService

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=None,
        responses={
            200: {
                "description": "New tokens generated successfully",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "data": {"accessToken": {"type": "string"},
                    "refreshToken": {"type": "string"}},
                    "info": {"type": "string"}
                }
            },
            400: {
                "description": "Token refresh failed",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"}
                }
            }
        },
        summary="Refresh JWT tokens",
        description="Expects a valid refresh token and returns a new access and refresh token."
    )
    @transaction.atomic
    def post(self, request):
        try:
            refresh_token = request.data.get("refreshToken")
            if not refresh_token:
                return api_response(
                    success=False,
                    info="REFRESH_TOKEN_REQUIRED",
                    error="Refresh token is required.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            new_tokens = UserService.refresh_tokens(refresh_token)

            return api_response(
                success=True,
                info="TOKENS_REFRESHED",
                data=new_tokens,
                status_code=status.HTTP_200_OK
            )

        except ValidationError as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="VALIDATION_ERROR",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except TokenError as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="INVALID_REFRESH_TOKEN",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            transaction.set_rollback(True)
            exception_log(e, __file__)
            return api_response(
                success=False,
                info="REFRESH_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
