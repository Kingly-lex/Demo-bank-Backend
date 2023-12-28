from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from rest_framework.exceptions import ValidationError
from werkzeug.security import generate_password_hash

from .models import Profile, NextOfKin


class CompleteProfileSerializer(serializers.ModelSerializer):
    transfer_pin = serializers.CharField(write_only=True, max_length=255)
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = ['phone_number', "gender", 'profile_photo', 'transfer_pin', 'verification_method',
                  'Verification_id', 'address', 'city', 'country', "marital_status", 'next_of_kin']

    def validate(self, attrs):
        user = self.context.get('request').user
        phone_number = attrs.get('phone_number', None)
        gender = attrs.get('gender', None)
        transfer_pin = attrs.get('transfer_pin', None)
        profile_photo = attrs.get('profile_photo', None)
        verification_method = attrs.get('verification_method', None)
        Verification_id = attrs.get('Verification_id', None)
        address = attrs.get('address', None)
        city = attrs.get('city', None)
        country = attrs.get('country', None)
        marital_status = attrs.get('marital_status', None)

        if user.profile.is_updated:
            raise ValidationError("User Profile has been Created and Completed, Please go to update route")

        if phone_number is None:
            raise ValidationError("phone_number field is required")

        if gender is None:
            raise ValidationError("gender field is required")

        if transfer_pin is None or len(transfer_pin) > 4:
            raise ValidationError("transfer_pin field is required and must not be more than 4 digits")

        if profile_photo is None:
            raise ValidationError("profile_photo field is required")

        if verification_method is None:
            raise ValidationError("verification_method field is required")

        if Verification_id is None:
            raise ValidationError("verification_id field is required")

        if address is None:
            raise ValidationError("address field is required")

        if city is None:
            raise ValidationError("city field is required")

        if country is None:
            raise ValidationError("country field is required")

        if marital_status is None:
            raise ValidationError("marital_status is required")

        if not transfer_pin.isdigit():
            raise ValidationError("transfer_pin field must be numericals")

        transfer_pin = generate_password_hash(transfer_pin, method="pbkdf2:sha256", salt_length=16)

        return super().validate(attrs)


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = ['phone_number', "gender", 'profile_photo',
                  'marital_status', 'next_of_kin', 'address', 'city', 'country']

    def validate(self, attrs):
        user = self.context.get('request').user

        if not user.profile.is_updated:
            raise ValidationError('You need to Complete Your profile First')

        return super().validate(attrs)


class RetrieveProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    profile_photo = serializers.SerializerMethodField()
    Verification_id = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'full_name', 'phone_number', 'account_no', 'account_balance', "gender",
                  'profile_photo', 'next_of_kin', 'marital_status', 'Verification_id', 'address', 'city', 'country']

    def get_full_name(self, obj):
        return obj.user.full_name.capitalize()

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

    def get_Verification_id(self, obj):

        try:
            return obj.Verification_id.url
        except Exception:
            return None


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', None)
        first_name = attrs.get('first_name', None)
        last_name = attrs.get('last_name', None)
        phone_number = attrs.get('phone_number', None)
        gender = attrs.get('gender', None)
        profile_photo = attrs.get('profile_photo', None)
        address = attrs.get('address', None)
        city = attrs.get('city', None)
        country = attrs.get('country', None)

        if email is None:
            raise ValidationError("email field is required")

        if first_name is None:
            raise ValidationError("first_name field is required")

        if last_name is None:
            raise ValidationError("last_name field is required")

        if phone_number is None:
            raise ValidationError("phone_number field is required")

        if gender is None:
            raise ValidationError("gender field is required")

        if profile_photo is None:
            raise ValidationError("profile_photo field is required")

        if address is None:
            raise ValidationError("address field is required")

        if city is None:
            raise ValidationError("city field is required")

        if country is None:
            raise ValidationError("country field is required")

        return super().validate(attrs)
