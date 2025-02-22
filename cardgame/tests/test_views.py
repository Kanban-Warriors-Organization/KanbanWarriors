"""
Test suite for view functionality and request handling.
Verifies correct behavior of all views including authentication,
card management, challenges, and user interactions.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from cardgame.models import Card, CardSet, UserProfile, Challenge, Question
from django.urls import reverse
from django.utils import timezone
import datetime
import json
from cardgame.views import *


class AuthenticationViewTests(TestCase):
    """
    Test suite for authentication-related views.
    Validates signup, login, and logout functionality.

    Author: Sam
    """

    def setUp(self):
        self.client = Client()
        self.test_user = {"username": "testuser", "password": "testpass123"}

    def test_signup_success(self):
        """Tests successful user registration process."""
        response = self.client.post(
            reverse("signup"),
            {
                "username": self.test_user["username"],
                "password1": self.test_user["password"],
                "password2": self.test_user["password"],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(username=self.test_user["username"]).exists()
        )

    def test_signup_duplicate_user(self):
        """Tests signup failure with existing username."""
        User.objects.create_user(**self.test_user)
        response = self.client.post(
            reverse("signup"),
            {
                "username": self.test_user["username"],
                "password1": self.test_user["password"],
                "password2": self.test_user["password"],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "you done goofed!")


class CardViewTests(TestCase):
    """
    Test suite for card-related views.
    Tests card collection display, card creation, and related functionality.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user, user_profile_points=0)
        self.card = Card.objects.create(
            card_name="Test Card",
            card_subtitle="Test Subtitle",
            card_description="Test Description",
        )

    def test_card_col_success(self):
        """Tests successful display of user's card collection."""
        self.profile.user_profile_collected_cards.add(self.card)
        response = self.client.get(reverse("card_col", args=["testuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/card_col.html")

    def test_card_col_nonexistent_user(self):
        """Tests card collection view with non-existent user."""
        response = self.client.get(reverse("card_col", args=["nonexistentuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")


class ChallengeViewTests(TestCase):
    """
    Test suite for challenge-related views.
    Validates challenge creation, display, and interaction functionality.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.card = Card.objects.create(
            card_name="Test Card",
            card_subtitle="Test Subtitle",
            card_description="Test Description",
        )
        self.challenge = Challenge.objects.create(
            card=self.card,
            latitude=51.5074,
            longitude=-0.1278,
            start_time=timezone.now(),
            end_time=timezone.now() + datetime.timedelta(days=1),
            points_reward=100,
            description="Test Challenge",
        )

    def test_get_locations(self):
        """Tests retrieval of challenge locations."""
        response = self.client.get(reverse("get_locations"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("locations", data)
        self.assertEqual(len(data["locations"]), 1)
        self.assertEqual(data["locations"][0]["name"], "Test Card")

    def test_challenges_view(self):
        """Tests the challenges overview page."""
        response = self.client.get(reverse("challenges"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/challenges.html")


class LeaderboardTests(TestCase):
    """
    Test suite for leaderboard functionality.
    Validates correct ordering and display of user rankings.
    """

    def setUp(self):
        self.client = Client()
        for i in range(6):
            user = User.objects.create_user(f"user{i}", password="12345")
            UserProfile.objects.create(user=user, user_profile_points=i * 100)

    def test_leaderboard_data(self):
        """Tests leaderboard data retrieval and ordering."""
        response = self.client.get(reverse("leaderboard_data"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)  # Should only return top 5
        self.assertEqual(data[0]["points"], 500)  # Highest points should be first
        self.assertEqual(data[4]["points"], 100)  # Lowest points in top 5


class ProfileViewTests(TestCase):
    """
    Test suite for user profile functionality.
    Validates profile display and management features.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(
            user=self.user, user_profile_points=100
        )

    def test_profile_view_success(self):
        """Tests successful profile display."""
        response = self.client.get(reverse("profile", args=["testuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profile of testuser")

    def test_profile_view_nonexistent_user(self):
        """Tests profile view with non-existent user."""
        response = self.client.get(reverse("profile", args=["nonexistentuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "failure!")
