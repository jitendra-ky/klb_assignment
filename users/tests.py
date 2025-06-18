"""Test cases for the users app."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class RegisterViewTest(APITestCase):
    """Tests for the RegisterView (user registration endpoint)."""

    def setUp(self) -> None:
        """Set up test data and client."""
        self.client = APIClient()
        self.register_url = reverse("register")
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_register_success(self) -> None:
        """Test successful user registration."""
        response = self.client.post(self.register_url, self.user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == self.user_data["username"]
        assert response.data["email"] == self.user_data["email"]
        assert "password" not in response.data

    def test_register_missing_fields(self) -> None:
        """Test registration with missing required fields."""
        data = self.user_data.copy()
        data.pop("email")
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data


class ProfileViewTest(APITestCase):
    """Tests for the ProfileView (user profile endpoint)."""

    def setUp(self) -> None:
        """Set up test data and client."""
        self.client = APIClient()
        self.register_url = reverse("register")
        self.profile_url = reverse("profile")
        self.user_data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpass456",
            "first_name": "Test2",
            "last_name": "User2",
        }
        # Register user for authentication tests
        self.client.post(self.register_url, self.user_data, format="json")

    def test_profile_unauthenticated(self) -> None:
        """Test accessing profile endpoint without authentication."""
        response = self.client.get(self.profile_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_authenticated(self) -> None:
        """Test accessing profile endpoint with authentication."""
        token_url = reverse("token_obtain_pair")
        token_response = self.client.post(
            token_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        assert token_response.status_code == status.HTTP_200_OK
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.profile_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user_data["username"]
        assert response.data["email"] == self.user_data["email"]
        assert "password" not in response.data
