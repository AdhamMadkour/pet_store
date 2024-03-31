import pytest
from rest_framework import status


@pytest.mark.django_db
class TestStoreEndpoints:
    def test_user_is_anonymous_returns_200(self, api_client):
        response = api_client.get("/store/")
        assert response.status_code == status.HTTP_200_OK
