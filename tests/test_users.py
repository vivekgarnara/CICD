import allure
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"
client = APIClient(BASE_URL)


@allure.feature("Test API")
class TestPytestDemo:
    @allure.story("Fetch Users")
    @allure.title("Get all users list")
    @allure.description(
        "Verify the get users API returns status 200 and contains user list with IDs"
    )
    @allure.severity("Critical")
    def test_get_users(self):
        response = client.get("/users?page=2")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]

    @allure.story("Fetch Posts")
    @allure.title("Get single post by ID")
    @allure.description(
        "Verify the get post API returns status 200 with correct post ID and title"
    )
    @allure.severity("Critical")
    def test_get_single_post(self):
        response = client.get("/posts/1")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == 1
        assert "title" in data

    @allure.story("Fetch Posts")
    @allure.title("Get posts filtered by user ID")
    @allure.description(
        "Verify the get posts API filters correctly by userId parameter and returns matching posts"
    )
    @allure.severity("Critical")
    def test_get_posts_by_user(self):
        params = {"userId": 1}
        response = client.get("/posts", params=params)

        assert response.status_code == 200
        data = response.json()

        for post in data:
            assert post["userId"] == 1

    @allure.story("HTTP Headers Handling")
    @allure.title("Get post with custom headers")
    @allure.description("Verify the API accepts custom headers and returns status 200")
    @allure.severity("Normal")
    def test_with_headers(self):
        headers = {"Content-Type": "application/json"}

        response = client.get("/posts/1", headers=headers)
        assert response.status_code == 200
