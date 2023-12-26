from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# local imports
from .serializers import (CompleteProfileSerializer, RetrieveProfileSerializer, UpdateProfileSerializer)
from .renderers import ProfileRenderer, ProfilesRenderer
from .models import Profile
from .utils import generate_account_no, send_account_number_notification


# async def update_profile(profile):
#     acct = generate_account_no()


class CreateCompleteProfile(GenericAPIView):
    serializer_class = CompleteProfileSerializer
    renderer_classes = [ProfileRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        acct = generate_account_no()
        profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(instance=profile, data=request.data, context={'request': request},)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            profile.is_updated = True
            profile.account_no = acct
            profile.save()
            send_account_number_notification(email=profile.user.email, acct_no=acct)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfile(GenericAPIView):
    serializer_class = UpdateProfileSerializer
    renderer_classes = [ProfileRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewProfile(RetrieveAPIView):
    serializer_class = RetrieveProfileSerializer
    renderer_classes = [ProfileRenderer]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile


class ViewAllCustomerProfiles(ListAPIView):
    serializer_class = RetrieveProfileSerializer
    renderer_classes = [ProfilesRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Profile.objects.all()
