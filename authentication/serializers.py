from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
# from .models import CustomUser

CustomUser = get_user_model()


# Login serializer
class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")
