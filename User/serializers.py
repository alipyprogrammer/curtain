from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ExpertPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = User.objects.create(password=hashed_password, **validated_data)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'token']
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
