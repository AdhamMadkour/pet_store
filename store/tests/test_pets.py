import json
import pytest
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import Category, Tags

TestPetData = {
    "name": "Test",
    "age": 3,
    "status": True,
    "price": "1200.00",
    "category": 1,
    "tags": [1],
}


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(user=None):
        if user is None:
            user = User.objects.create_user(
                username="test_user", password="test_password"
            )
        return api_client.force_authenticate(user=user)

    return do_authenticate


@pytest.mark.django_db
class TestPetEndpoints:
    def test_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get("/pets/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_authenticated_returns_403(self, api_client):
        api_client.force_authenticate(user={})
        response = api_client.get("/pets/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_authenticated_returns_200(self, api_client, authenticate):
        User = get_user_model()
        user = User.objects.create_user(username="test_user", password="test_password")
        authenticate(user=user)
        response = api_client.get("/pets/")
        assert response.status_code == status.HTTP_200_OK

    def test_create_pet_returns_created_201(self, api_client, authenticate):
        User = get_user_model()
        user = User.objects.create_user(username="test_user", password="test_password")
        Category.objects.create(name="Test")
        Tags.objects.create(name="Test")
        authenticate(user=user)
        response = api_client.post(
            "/pets/",
            data=json.dumps(TestPetData),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == TestPetData["name"]
        assert response.data["age"] == TestPetData["age"]
        assert response.data["status"] == TestPetData["status"]
        assert response.data["category"] == TestPetData["category"]
        assert response.data["tags"] == TestPetData["tags"]
        assert response.data["price"] == TestPetData["price"]
