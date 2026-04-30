import allure
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"
client = APIClient(BASE_URL)

@allure.feature("Test API")
class TestPytestDemo:

    @allure.story("Test get endpoint")
    @allure.title("Verify the get API")
    @allure.description("verify the get API response status code and data")
    @allure.severity("Critical")
    def test_get_users(self):
        response = client.get("/users?page=2")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]

    def test_get_single_post(self):
        response = client.get("/posts/1")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == 1
        assert "title" in data

    def test_get_posts_by_user(self):
        params = {"userId": 1}
        response = client.get("/posts", params=params)

        assert response.status_code == 200
        data = response.json()

        for post in data:
            assert post["userId"] == 1

    def test_with_headers(self):
        headers = {
            "Content-Type": "application/json"
        }

        response = client.get("/posts/1", headers=headers)
        assert response.status_code == 200