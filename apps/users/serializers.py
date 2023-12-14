from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id')
    email = serializers.CharField(source='email')
    username = serializers.CharField(source='username')
    full_name = serializers.SerializerMethodField()
    gender = serializers.CharField(source='profile.gender')
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'full_name',
            'gender',
            "phone_number",
            "profile_photo",
            "country",
            "city",
        ]

    def get_full_name(self, obj):
        return obj.full_name.capitalize()


class CreateUserSerializer(UserCreateSerializer):
    middle_name = serializers.CharField(source="user.middle_name", required=False)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "middle_name", "password",]
