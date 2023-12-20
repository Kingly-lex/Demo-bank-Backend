from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# custom
from .utils import send_verify_email_otp, create_jwt_pair_for_user, send_password_reset_otp
from .models import User, OTPForUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=100, min_length=1)
    first_name = serializers.CharField(max_length=100, min_length=1,)
    last_name = serializers.CharField(max_length=100, min_length=1)
    middle_name = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    password_confirm = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'password',
            'password_confirm',
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise ValidationError('Passwords do not Match, Please try again')
        return super().validate(attrs)

    def create(self, validated_data):
        middle_name = validated_data.get("middle_name", '')
        email = validated_data.get('email')

        user = User.objects.create_user(email=email,
                                        username=validated_data.get('username'),
                                        first_name=validated_data.get('first_name'),
                                        last_name=validated_data.get('last_name'),
                                        middle_name=middle_name,
                                        password=validated_data.get('password'),
                                        )

        send_verify_email_otp(email)

        return user


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True, required=True)
    full_name = serializers.CharField(max_length=100, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', "full_name", 'access_token', 'refresh_token']
        read_only_fields = ['id']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        if not User.objects.filter(email=email).exists():
            raise AuthenticationFailed('User does not exist, Please register')

        user = authenticate(request=request, email=email, password=password)

        if user is None:
            raise AuthenticationFailed('Incorrect password, try again')

        if not user.is_verified:
            raise AuthenticationFailed(
                "You account email hasn't been verified, please verify your account to continue")

        tokens = create_jwt_pair_for_user(user=user)

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "access_token": tokens.get('access_token'),
            "refresh_token": tokens.get('refresh_token'),

        }


class LogoutSerilaizer(serializers.Serializer):
    token = serializers.CharField(required=True, write_only=True)

    default_error_messages = {"bad_token": ('Token is expired or invalid')}

    def validate(self, attrs):
        if not attrs.get('token'):
            raise ValueError('Token must be provided')
        return super().validate(attrs)

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')


class ActivateSerializer(serializers.Serializer):
    """
       Activates a new account after user registration,

       All accounts must be activated/verified before they can login.
    """
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6)

    def validate(self, attrs):
        email = attrs.get('email', None)
        code = attrs.get('code', None)

        if email is None or code is None:
            raise ValueError('Email and OTP fields must be Provided')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('You do not have an account with us')

        user = User.objects.get(email=email)

        if OTPForUser.objects.filter(email_otp=code, user=user).exists():
            if user.is_verified:
                raise ValidationError("account is already verified")

            user.is_verified = True
            user.save()
        return super().validate(attrs)


class RequestNewActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email', None)

        if email is None:
            raise ValueError('Email field must be Provided')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('You do not have an account with us')

        return {'email': email}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        request = self.context.get('request')

        if email is None:
            raise ValueError('Email field must be Provided')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('You do not have an account with us')

        send_password_reset_otp(email, request)

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """
    For validated/logged in users to change their passwords

    """
    old_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    password_confirm = serializers.CharField(max_length=100, min_length=6, write_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        temp_user = request.user
        temp_email = temp_user.email

        if password != password_confirm:
            raise ValidationError('Passwords do not Match, Please try again')

        user = authenticate(request=request, email=temp_email, password=old_password)
        if user is not None:
            user.set_password(password)
            user.save()
            return user
        raise AuthenticationFailed('Incorrect password, try again')


class SetNewPasswordSerializer(serializers.Serializer):
    """
    For reseting passwords for users who forgot theirs

    """
    token = serializers.CharField(max_length=255, write_only=True, required=True)
    uidb64 = serializers.CharField(max_length=100, write_only=True, required=True)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True, required=True)
    password_confirm = serializers.CharField(max_length=100, min_length=6, write_only=True, required=True)

    def validate(self, attrs):
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise ValidationError('Passwords do not Match, Please try again')

        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(token=token, user=user):
                user.set_password(password)
                user.save()
                return user
            return AuthenticationFailed(
                "Failed token, expired or invalid")
        except Exception:
            raise AuthenticationFailed(
                "Reset link is invalid or has expired")
