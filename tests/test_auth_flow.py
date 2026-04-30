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