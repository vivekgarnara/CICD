import pytest
from utils.api_client import APIClient

BASE_URL = "https://dummyjson.com"


@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL)


@pytest.fixture(scope="session")
def auth_token(api_client):

    login_payload = {
        "username": "emilys",
        "password": "emilyspass",
        "expiresInMins": 30,
    }

    response = api_client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    token = response.json()["accessToken"]
    return token
