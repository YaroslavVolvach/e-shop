from rest_framework import serializers
from account.models import CustomUser
from django.contrib.auth.hashers import make_password


class RegistrationAPISerialazer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'password')


class UserAPISerialazer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = (
            'is_staff',
            'is_active',
            'email',
            'user_name',
            'country',
            'city',
            'date_joined',
            'gender',
            'main_image',
            'password',
            'id'
        )

        read_only_fields = ('is_staff', 'is_active', 'date_joined')


class UserBanOrUnbanAPISerialazer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('is_active', 'email', 'user_name', 'id')

        read_only_fields = ('user_name', 'email')


class ChangePermissionAPISerialazer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('is_staff', 'email', 'user_name', 'id')

        read_only_fields = ('user_name', 'email')
