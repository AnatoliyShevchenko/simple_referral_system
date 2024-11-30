# Django Rest Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

# SimpleJWT
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Third-Party
from drf_yasg.utils import swagger_auto_schema
from loguru import logger

# Django
from django.db.models import Q
from django.utils import timezone

# Python
import random
import time

# Local
from .models import User
from .serializers import \
    PhoneNumberSerializer, AuthCodeSerializer, TokensSerializer


@permission_classes([AllowAny])
class AuthView(TokenObtainPairView):
    """Custom authorization with validation fields."""

    @swagger_auto_schema(
        request_body=PhoneNumberSerializer, 
        responses={
            200: "Your authenticate code has been sent to your phone! " 
            "(0000) It's active only for 2 minutes!" , 
            409: "Conflict creating or finding user."
        } 
    )
    def post(self, request: Request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        user, _ = User.objects.get_or_create(phone=phone_number)
        if not user: 
            logger.error("Conflict creating or finding user "
                         "with phone number {phone_number}.")
            return Response(
                data={"detail": "Conflict creating or finding user."}, 
                status=status.HTTP_409_CONFLICT 
            )
        auth_code = user.set_auth_code() 
        response_data = {
            "message": "Your authenticate code has been sent to your phone! " 
            f"({auth_code}) It's active only for 2 minutes!" 
        }
        time.sleep(random.randint(1,2))
        return Response(
            data=response_data, status=status.HTTP_200_OK
        ) 

    @swagger_auto_schema(
        request_body=AuthCodeSerializer, 
        responses={
            200: TokensSerializer, 
            404: "Auth code is invalid or expired.",
            406: "Token generation failed"
        } 
    )
    def patch(self, request: Request):
        serializer = AuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_code = serializer.validated_data.get("auth_code")
        try:
            user: User = User.objects.get(
                Q(auth_code=auth_code), 
                Q(auth_code_expires__gt=timezone.now())
            )
            if not user.is_active:
                user.is_active=True
                user.save()
            try:
                refresh_token = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)
                response_serializer = TokensSerializer(data={
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token)
                })
                response_serializer.is_valid()
            except TokenError as te:
                logger.error(f"Token generation failed: {te}")
                return Response(
                    data={"error": "Token generation failed"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            return Response(
                data=response_serializer.data, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND, 
                data={"detail": "Auth code is invalid or expired"}
            )
