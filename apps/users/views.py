from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


# custom imports
from .serializers import (RegisterSerializer, LoginSerializer, LogoutSerilaizer, ActivateSerializer,
                          RequestNewActivationSerializer, ChangePasswordSerializer, SetNewPasswordSerializer,
                          ForgotPasswordSerializer)
from .utils import send_verify_email_otp


User = get_user_model()


class RegisterView(GenericAPIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True,
                             'response': "User created successfully, Please check inbox to verify your email"},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors,
                         'success': False,
                         'response': "Invalid credentials"},
                        status=status.HTTP_403_FORBIDDEN)


class ActivateAccount(GenericAPIView):
    serializer_class = ActivateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'response': 'Account email verified successfully'
                             }, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerilaizer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serilizer = self.serializer_class(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            return Response({"success": True,
                             "response": "you have logged out"},
                            status=status.HTTP_204_NO_CONTENT)


class Request_new_verification_email(GenericAPIView):
    serializer_class = RequestNewActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            send_verify_email_otp(email)
            return Response({'success': True,
                            "response": 'A new code has been sent to your email'})


class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True,
                            "response": 'Password change was successful'}, status=status.HTTP_200_OK)


class ForgotPassword(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True,
                            "response": 'Instructions have been sent to your email'}, status=status.HTTP_202_ACCEPTED)


class SetNewPassword(GenericAPIView):
    permission_classes = []
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'response': 'Account password has been successfully reset'
                             }, status=status.HTTP_200_OK)
        return Response({'success': False, 'response': 'Bad request'}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetConfirmWeb(GenericAPIView):
    pass
