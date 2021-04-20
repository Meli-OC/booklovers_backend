from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
# from .models import CustomUser

CustomUser = get_user_model()


# register Serializer
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    # Define the transaction.atomic to rollback the save operation in of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name  = self.data.get('last_name')
        user.save()
        return user


# Login serializer
class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# User serializer
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("pk", "username", "email", "first_name", "last_name")
        read_only_fields = ("pk", )

