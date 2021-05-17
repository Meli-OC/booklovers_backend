from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
# from .models import CustomUser

CustomUser = get_user_model()


# User  details serializer
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("pk", "username", "email", "first_name", "last_name")
        read_only_fields = ("pk", )

