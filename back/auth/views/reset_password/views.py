from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from cryptography.fernet import Fernet, InvalidToken
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.db import transaction
from django.utils import timezone
from core.utils.logger import exception_log
from core.models import  Language, User
from auth.serializers.register import RegisterSerializer
from auth.services.user_service import UserService
from core.utils.response_wrapper import api_response
import json
            
fernet = Fernet(settings.ENCRYPTION_KEY)

# class ForgetPasswordView(APIView):
#     authentication_classes = []

#     @extend_schema(
#         request=ResendCodeSerializer,
#         responses={
#             201: {
#                 "description": "Reset code sent successfully",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "info": {"type": "string"}
#                 }
#             },
#             400: {
#                 "description": "Code sending failed",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "info": {"type": "string"},
#                     "error": {"type": "string"}
#                 }
#             }
#         },
#         summary="Reset password code sending",
#         description="Sends reset password email with pin code."
#     )
#     @transaction.atomic
#     def post(self, request):
#         try:
#             email = request.data.get("email")
#             if not email:
#                 return api_response(
#                     success=False,
#                     info="EMAIL_REQUIRED",
#                     error="Email field is required.",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )

#             user = User.objects.filter(email=email).first()
#             #TODO: search for either to keep like this or send (verify your account message when user is registered not verified)
#             if not user.is_active or not user:
#                 return api_response(
#                     success=True,
#                     info="RESET_CODE_SENT",
#                     status_code=status.HTTP_201_CREATED
#                 )

#             pin_code = PinCodeService.create_pin(user, 'reset_password', 4)
#             current_year = timezone.now().year

#             email_data = {
#                 'user_first_name': user.first_name,
#                 'year': current_year,
#                 'code': pin_code,
#                 'expiry_time': 30,  
#             }

#             EmailService.send_email(
#                 user.email, 
#                 "Reset you password", 
#                 "reset_password.html", 
#                 email_data
#             )

#             return api_response(
#                 success=True,
#                 info="RESET_CODE_SENT",
#                 status_code=status.HTTP_201_CREATED
#             )

#         except ValidationError as e:
#             transaction.set_rollback(True)
#             exception_log(e, __file__)
#             return api_response(
#                 success=False,
#                 info="VALIDATION_ERROR",
#                 error=str(e),
#                 status_code=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             transaction.set_rollback(True)
#             exception_log(e, __file__)
#             return api_response(
#                 success=False,
#                 info="RESET_FAILED",
#                 error=str(e),
#                 status_code=status.HTTP_400_BAD_REQUEST
#             )

# class ResetPasswordView(APIView):
#     authentication_classes = []
    
#     @extend_schema(
#         request=RegisterSerializer,
#         responses={
#             200: {
#                 "description": "Password reseted successfully",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "info": {"type": "string"}
#                 }
#             },
#             400: {
#                 "description": "Reset failed",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "info": {"type": "string"},
#                     "error": {"type": "string"}
#                 }
#             }
#         },
#         summary="Reset a user password",
#         description="Reset a user password."
#     )
#     @transaction.atomic
#     def post(self, request):
#         try:
#             newPassword = request.data.get('newPassword')
#             token = request.data.get('token')
            
#             decrypted = fernet.decrypt(token.encode())
#             payload = json.loads(decrypted)
            

#             exp_timestamp = payload.get("exp")
#             if not exp_timestamp:
#                 return api_response(
#                     success=False,
#                     info="Invalid token payload",
#                     error="Invalid token payload",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )

#             if timezone.now().timestamp() > exp_timestamp:
#                 return api_response(
#                     success=False,
#                     info="Token expired",
#                     error="Token expired",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
#             email = payload.get("email")
            
#             if (str(token).strip() != str(latest_pin_code.token).strip()) or \
#             (str(email).strip().lower() != str(latest_pin_code.user.email).strip().lower()):
#                 return api_response(
#                     success=False,
#                     info="Invalid token payload",
#                     error="Invalid token payload",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
            
            
#             user = User.objects.get(email=email)

            

#             if not user.is_active:
#                 return api_response(
#                     success=False,
#                     info="USER_NOT_VALIDATED",
#                     error="The user account is not validated",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
                        
#             if not latest_pin_code:
#                 return api_response(
#                     success=False,
#                     info="INVALID_CODE",
#                     error="The activation code is invalid",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
        
#             if latest_pin_code.is_expired(5):
#                 return api_response(
#                     success=False,
#                     info="EXPIRED_CODE",
#                     error="The activation code has expired",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
            
#             UserService.reset_password(user,newPassword)
#             PinCodeService.use_pin(user, latest_pin_code, 'reset_password')

#             return api_response(
#                 success=True,
#                 info="PASSWORD_RESETED_SUCCESSFULLY",
#                 status_code=status.HTTP_200_OK
#             )
            
        # except Exception as e:
        #     transaction.set_rollback(True)
        #     exception_log(e, __file__)
        #     return api_response(
        #         success=False,
        #         info="ACTIVATION_FAILED",
        #         error="An error occurred during activation. Please try again.",
        #         status_code=status.HTTP_400_BAD_REQUEST
        #     )
            
            
# class VerifyPasswordCodeView(APIView):
#     authentication_classes = []
    
#     @extend_schema(
#         request=ActivationCodeSerializer,
#         responses={
#             200: {
#                 "description": "PCode Verified",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "data": {
#                         "type": "object",
#                         "properties": {
#                             "token": {"type": "string"}
#                         }
#                     },
#                     "info": {"type": "string"}
#                 }
#             },
#             400: {
#                 "description": "Reset failed",
#                 "type": "object",
#                 "properties": {
#                     "success": {"type": "boolean"},
#                     "info": {"type": "string"},
#                     "error": {"type": "string"}
#                 }
#             }
#         },
#         summary="Reset a code and email",
#         description="Verify a reset password code."
#     )
#     @transaction.atomic
#     def post(self, request):
#         try:
#             email = request.data.get('email')
#             code = request.data.get('code')
#             user = User.objects.get(email=email)

            
#             latest_pin_code = PinCodeService.get_latest__pin(user, 'reset_password', code)

#             if not user.is_active:
#                 return api_response(
#                     success=False,
#                     info="USER_NOT_VALIDATED",
#                     error="The user account is not validated",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
                        
#             if not latest_pin_code:
#                 return api_response(
#                     success=False,
#                     info="INVALID_CODE",
#                     error="The activation code is invalid",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
        
#             if latest_pin_code.is_expired(5):
#                 return api_response(
#                     success=False,
#                     info="EXPIRED_CODE",
#                     error="The activation code has expired",
#                     status_code=status.HTTP_400_BAD_REQUEST
#                 )
            
#             token  =  PinCodeService.add_token_to_pin(latest_pin_code)

#             return api_response(
#                 success=True,
#                 info="CODE VERIFIED",
#                 data={
#                     "token": token
#                 },   
#                 status_code=status.HTTP_200_OK
#             )
            
#         except Exception as e:
#             transaction.set_rollback(True)
#             exception_log(e, __file__)
#             return api_response(
#                 success=False,
#                 info="ACTIVATION_FAILED",
#                 error="An error occurred during activation. Please try again.",
#                 status_code=status.HTTP_400_BAD_REQUEST
#             )

