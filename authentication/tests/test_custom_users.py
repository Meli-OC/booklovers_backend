import pytest
from django.contrib.auth import get_user_model
# from authentication.models import CustomUser

CustomUser = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(email="test@test.com", username="test", password="test12345")
    assert user.email == "test@test.com"
    assert user.username == "test"
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False
    assert str(user) == user.email


@pytest.mark.django_db
def test_create_superuser():
    admin_user = CustomUser.objects.create_superuser(email="supertest@test.com", username="admin", password="mysuperpassword")
    assert admin_user.email == "supertest@test.com"
    assert admin_user.is_active == True
    assert admin_user.is_staff == True
    assert admin_user.is_superuser == True
