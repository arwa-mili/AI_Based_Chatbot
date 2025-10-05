from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from django.db import transaction
from core.utils.logger import exception_log
from core.utils.response_wrapper import api_response
from auth.serializers.profile import UserProfileSerializer, UserProfileUpdateSerializer
from auth.services.user_service import UserService


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["profile"],
        responses={
            200: UserProfileSerializer,
            400: {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "info": {"type": "string"},
                    "error": {"type": "string"},
                },
            },
        },
        summary="Get current user profile",
        description="Returns the profile data of the authenticated user."
    )
    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)

            return api_response(
                success=True,
                info="USER_FETCHED",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            exception_log(e, __file__, log_info="Failed to fetch user")
            return api_response(
                success=False,
                info="USER_FETCH_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


    @extend_schema(
        tags=["profile"],
        request=UserProfileUpdateSerializer,
        responses=UserProfileSerializer,
        summary="Update current user profile",
        description="Updates the authenticated user's profile fields. Partial updates are supported."
    )
    @transaction.atomic
    def put(self, request):
        try:
            user = request.user

            serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            updated_user = UserService.update_user_profile(
                user, 
                serializer.validated_data,
                request.data
            )

            return api_response(
                success=True,
                info="USER_UPDATED",
                data={"user": UserProfileSerializer(updated_user).data},
                status_code=status.HTTP_200_OK
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
            exception_log(e, __file__, log_info="Failed to update user")
            return api_response(
                success=False,
                info="USER_UPDATE_FAILED",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
