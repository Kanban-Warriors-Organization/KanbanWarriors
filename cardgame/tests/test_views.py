from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from cardgame.models import Card, CardSet, UserProfile, Challenge

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a normal user and user profile for testing
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user_profile = UserProfile.objects.create(user=self.user, user_profile_points=50)
        # Create a staff user for create_card view
        self.staff_user = User.objects.create_user(username="staffuser", password="staffpass")
        self.staff_user.is_staff = True
        self.staff_user.save()
        # Create a CardSet and a Card for testing
        self.card_set = CardSet.objects.create(card_set_name="TestSet", card_set_description="A test set")
        self.card = Card.objects.create(
            card_name="TestCard",
            card_subtitle="Subtitle",
            card_description="Description",
            card_set=self.card_set
        )
        # Ensure the card is in the system for recent_card_data view
        self.card.save()
        # Create a Challenge that is active
        now = timezone.now()
        self.challenge = Challenge.objects.create(
            challenge_name="TestChallenge",
            description="A test challenge",
            start_time=now - datetime.timedelta(hours=1),
            end_time=now + datetime.timedelta(hours=1),
            longitude=10.0,
            latitude=20.0,
            card=self.card,
            points_reward=15,
            status='ongoing'
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("index page test", response.content.decode())

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/home.html")

    def test_signup_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfmiddlewaretoken", response.content.decode())

    def test_signup_post(self):
        post_data = {
            "username": "newuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123"
        }
        response = self.client.post(reverse("signup"), post_data)
        # on success, our view returns a simple HttpResponse with success message
        self.assertEqual(response.status_code, 200)
        self.assertIn("you did good", response.content.decode())

    def test_card_collection_view(self):
        # First add the card to the user profile so that card collection shows it in imgs_has.
        self.user_profile.user_profile_collected_cards.add(self.card)
        url = reverse("cardcollection", kwargs={"user_name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check that the owned cards appear in rendered context by ensuring the image link is referenced
        self.assertIn(self.card.card_image_link.url if self.card.card_image_link else "", response.content.decode())

    def test_recent_card_data(self):
        response = self.client.get(reverse("recent_card_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["name"], self.card.card_name)
        self.assertEqual(json_data["description"], self.card.card_description)
        # Ensure image key exists even if default image is used
        self.assertIn("image", json_data)

    def test_get_locations(self):
        response = self.client.get(reverse("locations_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("locations", json_data)
        # Check that our test challenge's card name appears in the locations
        self.assertTrue(any(loc["name"] == self.card.card_name for loc in json_data["locations"]))

    def test_leaderboard_data(self):
        # Create additional user profiles for leaderboard test
        user2 = User.objects.create_user(username="user2", password="pass2")
        UserProfile.objects.create(user=user2, user_profile_points=100)
        response = self.client.get(reverse("leaderboard_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIsInstance(json_data, list)
        # Check that at most 5 players are returned
        self.assertLessEqual(len(json_data), 5)
        # Verify that the top player's points are in descending order
        if len(json_data) > 1:
            self.assertGreaterEqual(json_data[0]["points"], json_data[1]["points"])

    def test_profile_view(self):
        url = reverse("profile", kwargs={"user_name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile of " + self.user.username, response.content.decode())

    def test_challenges_view(self):
        response = self.client.get(reverse("challenges"))
        self.assertEqual(response.status_code, 200)
        # The rendered page should include our challenge details (e.g. card name)
        self.assertIn(self.card.card_name, response.content.decode())

    def test_challenge_detail_view(self):
        url = reverse("challenge", kwargs={"chal_id": self.challenge.id})
        response = self.client.get(url)
        # As the view is not fully implemented, our test confirms it returns failure
        self.assertEqual(response.status_code, 200)
        self.assertIn("failure!", response.content.decode())

    def test_create_card_get(self):
        # Test access without login should redirect to the login page (staff_member_required)
        response = self.client.get(reverse("create_card"))
        # Since we are not logged in as staff, we expect a redirection.
        self.assertNotEqual(response.status_code, 200)

    def test_create_card_post(self):
        # Log in as staff user to access create_card view
        self.client.login(username="staffuser", password="staffpass")
        with open("static/card_images/do_not_remove.py", "rb") as img:
            post_data = {
                "card_name": "NewCard",
                "card_subtitle": "NewSubtitle",
                "card_description": "NewDescription",
                "card_set": self.card_set.card_set_name,
                "card_image": img,
            }
            response = self.client.post(reverse("create_card"), post_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Card created successfully", response.content.decode())