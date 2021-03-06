from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """ Personalization of the class UserCreationForm to create new user"""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    """ Personalization of the class UserChangeForm to allow user's updates"""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',)
