import json
import pytest
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import Category, Tags, Pet

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
class TestAuctionEndpoints:
    def test_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get("/auction/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_auction_if_user_is_owner_returns_201(
        self, api_client, authenticate
    ):
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
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_auction_if_user_is_not_owner_returns_403(
        self, api_client, authenticate
    ):
        User = get_user_model()
        user = User.objects.create_user(username="test_user", password="test_password")
        authenticate(user=user)
        Pet.objects.create(
            owner=User.objects.create_user(
                username="test_owner", password="test_password"
            ),
            name="Test",
            age=3,
            status=True,
            price="1200.00",
            category=Category.objects.create(name="Test"),
        )
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_auction_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_auction_if_user_is_not_authenticated_returns_403(
        self, api_client, authenticate
    ):
        authenticate(user={})
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_auction_if_already_created_for_animal_returns_400(
        self, api_client, authenticate
    ):
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
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = api_client.post(
            "/auction/",
            data=json.dumps(
                {
                    "pet": 1,
                    "start_price": "1000.00",
                    "start_date": "2021-09-01T00:00:00Z",
                    "end_date": "2021-09-30T00:00:00Z",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
