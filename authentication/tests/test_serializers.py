import pytest
from authentication.serializers import CustomRegisterSerializer, CustomUserDetailsSerializer

@pytest.mark.django_db
def test_valid_CustomSerializer():
    valid_serializer_data = {
        "pk": 1,
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