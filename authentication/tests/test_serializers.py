import pytest
from authentication.serializers import CustomRegisterSerializer, CustomUserDetailsSerializer


@pytest.mark.django_db
def test_valid_custom_serializer():
    valid_serializer_data = {
        "username": "test",
        "email": "test@test.com",
        "first_name": "toto",
        "last_name": "dupont"
    }

    serializer = CustomUserDetailsSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_custom_serializer():
    invalid_serializer_data = {
        "email": "test@test.com",
        "first_name": "toto",
        "last_name": "dupont"
    }

    serializer = CustomUserDetailsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {'username': ['This field is required.']}