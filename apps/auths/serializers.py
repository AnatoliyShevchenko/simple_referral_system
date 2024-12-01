# RestFramework
from rest_framework import serializers

# Django
from django.core.validators import \
    RegexValidator, MinLengthValidator, MaxLengthValidator

# Local
from .models import User


VALIDATE_PATTERN = r'^\+\d{1}\d{3}\d{3}\d{2}\d{2}$' 
PHONE_NUMBER_VALIDATOR = [
    RegexValidator(
        VALIDATE_PATTERN, 
        message="""phone_number must be in format "+00000000000"."""
    )
]

class PhoneNumberSerializer(serializers.Serializer):
    """Serializer for custom auth view."""

    phone_number = serializers.CharField(
        required=True, validators=PHONE_NUMBER_VALIDATOR
    )

    def validate(self, attrs):
        return super().validate(attrs)
    

class AuthCodeSerializer(serializers.Serializer):
    auth_code = serializers.CharField(validators=[
        MinLengthValidator(
            limit_value=4, message="Auth code must be equal 4 symbols"
        ),
        MaxLengthValidator(
            limit_value=4, message="Auth code must be equal 4 symbols"
        )
    ])


class TokensSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class InvitedUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей, которых пригласил текущий пользователь."""

    class Meta:
        model = User
        fields = ["invite_code", "phone"]


class UserSerializer(serializers.ModelSerializer):
    inviter = InvitedUserSerializer()
    invited_users = InvitedUserSerializer(many=True)

    class Meta:
        model = User
        fields = ["phone", "invite_code", "inviter", "invited_users"]


class InviterSerializer(serializers.Serializer):
    invited_by = serializers.CharField(validators=[
        MinLengthValidator(
            limit_value=6, message="Invite code must be equal 6 symbols"
        ),
        MaxLengthValidator(
            limit_value=6, message="Invite code must be equal 6 symbols"
        )
    ])
