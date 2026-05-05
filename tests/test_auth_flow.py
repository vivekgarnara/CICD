import allure
import json
import pytest

def load_login_data():
    with open("test_data/login_data.json") as f:
        return json.load(f)

@allure.feature("Test Advanced Auth Flow")
class TestAdvancedAuthFlow:

    @allure.story("Test login endpoint")
    @allure.title("Verify the login API")
    @allure.description("verify the login API response status code and data")
    @allure.severity("Critical")
    @pytest.mark.parametrize("data", load_login_data())
    def test_login_success(self, api_client, data):
        payload = {
            "username": data["username"],
            "password": data["password"],
            "expiresInMins": 30
        }

        response = api_client.post("/auth/login", json=payload)
        assert response.status_code == data["expected_status"]
        if response.status_code == 200:
            data = response.json()
            assert "accessToken" in data
            assert data["username"] == "emilys"

    @allure.story("Test get current user endpoint")
    @allure.title("Verify the get current user API")
    @allure.description("verify the get current user API response status code and data")
    @allure.severity("Critical")
    def test_get_current_user(self, api_client, auth_token):
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response = api_client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "emilys"

    @allure.story("Test login endpoint")
    @allure.title("Verify login with invalid credentials")
    @allure.description("Verify the login API returns 400 for invalid username/password")
    @allure.severity("Critical")
    def test_login_invalid_credentials(self, api_client):
        payload = {
            "username": "invaliduser",
            "password": "wrongpass",
            "expiresInMins": 30
        }

        response = api_client.post("/auth/login", json=payload)
        assert response.status_code == 400

    @allure.story("Test login endpoint")
    @allure.title("Verify login with missing username")
    @allure.description("Verify the login API returns error for missing username field")
    @allure.severity("Major")
    def test_login_missing_username(self, api_client):
        payload = {
            "password": "emilyspass",
            "expiresInMins": 30
        }

        response = api_client.post("/auth/login", json=payload)
        assert response.status_code == 400

    @allure.story("Test login endpoint")
    @allure.title("Verify login with missing password")
    @allure.description("Verify the login API returns error for missing password field")
    @allure.severity("Major")
    def test_login_missing_password(self, api_client):
        payload = {
            "username": "emilys",
            "expiresInMins": 30
        }

        response = api_client.post("/auth/login", json=payload)
        assert response.status_code == 400

    @allure.story("Test get current user endpoint")
    @allure.title("Verify get current user without token")
    @allure.description("Verify the get current user API returns 401 when no auth token provided")
    @allure.severity("Critical")
    def test_get_current_user_no_token(self, api_client):
        response = api_client.get("/auth/me")
        assert response.status_code == 401

    @allure.story("Test get current user endpoint")
    @allure.title("Verify get current user with invalid token")
    @allure.description("Verify the get current user API returns 401 for invalid auth token")
    @allure.severity("Critical")
    def test_get_current_user_invalid_token(self, api_client):
        headers = {
            "Authorization": "Bearer invalidtoken123"
        }

        response = api_client.get("/auth/me", headers=headers)
        assert response.status_code == 401