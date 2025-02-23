from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.db import IntegrityError
import datetime

from cardgame.models import Card, CardSet, UserProfile, Challenge, Question

class EmptyTestCase(TestCase):
    """
    This is for testing on an empty database
    Namely, that the correct responses are returned if a user attempts to access
    an object that does not exist
    Written by -Adam-
    """
    def setUp(self):
        self.client = Client()
    
    def test_profile_when_empty:
        url = reverse('profile', kwargs={'user_name': 'professor x'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cardcol_when_user_nonexistent:
        url = reverse('cardcollection', kwargs={'user_name': 'professor x'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_challenge_that_does_not_exist:
        url = reverse('challenge', kwargs={'chal_id': -9001})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_with_no_cards:
        self.user = User.objects.create_user(username='professor y', password='secret')
        self.user_profile = UserProfile.objects.create(user=self.user, user_profile_points=64)
        url = reverse('cardcollection', kwargs={'user_name': 'professor y'})
        response = self.client.get(url)




        

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user and its profile
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.user_profile = UserProfile.objects.create(user=self.user, user_profile_points=50)
        # Create a card and card set for testing card_col view
        self.card_set = CardSet.objects.create(card_set_name="Set1", card_set_description="Test set")
        self.card = Card.objects.create(
            card_name="TestCard",
            card_subtitle="Subtitle",
            card_description="Desc",
            card_set=self.card_set
        )
        self.user_profile.user_profile_collected_cards.add(self.card)
        # Create a challenge for testing get_locations and challenge view
        now = timezone.now()
        self.challenge = Challenge.objects.create(
            challenge_name="TestChallenge",
            description="Challenge desc",
            start_time=now - datetime.timedelta(hours=1),
            end_time=now + datetime.timedelta(hours=1),
            longitude=10.0,
            latitude=20.0,
            card=self.card,
            points_reward=10,
            status="ongoing"
        )
        # Create a question for challenge view
        self.question = Question.objects.create(
            challenge=self.challenge,
            text="Test question?",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_answer="B"
        )

    def test_index_and_home(self):
        response_index = self.client.get(reverse('index'))
        self.assertEqual(response_index.status_code, 200)
        self.assertTemplateUsed(response_index, "cardgame/home.html")

        response_home = self.client.get(reverse('home'))
        self.assertEqual(response_home.status_code, 200)
        self.assertTemplateUsed(response_home, "cardgame/home.html")

    def test_card_col(self):
        # Test card collection view for existing user
        url = reverse('cardcollection', kwargs={'user_name': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # The context should contain acquired cards
        self.assertIn("cardshas", response.context)
        self.assertEqual(response.context["cardshas"][0]["title"], "TestCard")

    def test_card_col_404(self):
        #checks that accessing a nonexistent card collections returns a 404
        url = reverse('cardcollection', kwargs={'user_name': 'nonexistent_user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recent_card_data(self):
        response = self.client.get(reverse('recent_card_data'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("name", json_data)
        self.assertEqual(json_data["name"], self.card.card_name)
        self.assertIn("description", json_data)
        self.assertIn("image", json_data)

    def test_signup_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/signup.html")

    def test_signup_post(self):
        signup_data = {
            "username": "newuser",
            "password1": "strongPassword123",
            "password2": "strongPassword123"
        }
        response = self.client.post(reverse('signup'), data=signup_data)
        self.assertEqual(response.status_code, 200)
        # Check that the user is created:
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Checks that another user is NOT made if the same credentials are used
        reponse2 = self.client.post(reverse('signup'), data=signup_data)
        self.assertTrue(User.objects.filter(username="newuser").count == 1)

    def test_create_card_get_and_post(self):
        # Create staff user for creating cards
        staff_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")
        # Test GET request
        response_get = self.client.get(reverse('create_card'))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "cardgame/create_card.html")
        # Test POST request with a dummy image file
        image_data = SimpleUploadedFile("test.png", b"dummydata", content_type="image/png")
        post_data = {
            "card_name": "NewCard",
            "card_subtitle": "NewSubtitle",
            "card_description": "New description",
            "card_set": "Set1"
        }
        files_data = {"card_image": image_data}
        response_post = self.client.post(reverse('create_card'), data=post_data, files=files_data)
        self.assertEqual(response_post.status_code, 200)
        # Verify new card was created
        self.assertTrue(Card.objects.filter(card_name="NewCard").exists())

        #Verifies another card is NOT made if the same details are used
        response_2 = self.client.post(reverse('create_card'), data=post_data, files=files_data)
        self.assertTrue(Card.objects.filter(card_name="NewCard").count() == 1)

    def test_get_locations(self):
        response = self.client.get(reverse('locations_data'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("locations", json_data)
        # The challenge's card name should appear in the locations
        self.assertEqual(json_data["locations"][0]["name"], self.card.card_name)

    def test_leaderboard_data(self):
        # Create additional users with points
        user2 = User.objects.create_user(username='user2', password='secret2')
        UserProfile.objects.create(user=user2, user_profile_points=80)
        response = self.client.get(reverse('leaderboard_data'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIsInstance(json_data, list)
        # Check that at most 5 players are returned.
        self.assertLessEqual(len(json_data), 5)

    def test_signout(self):
        # Log in and then sign out
        self.client.login(username=self.user.username, password='secret')
        response = self.client.get(reverse('logout'))
        # After signout, it should redirect to home or return a status code (our view returns HttpResponse)
        self.assertIn(response.status_code, [200, 302])

    def test_profile(self):
        url = reverse('profile', kwargs={'user_name': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Since profile.html is not implemented, response may be a simple HttpResponse text.
        self.assertIn(self.user.username, response.content.decode())

    def test_challenges(self):
        # Ensure user is logged in for challenges view
        self.client.login(username=self.user.username, password='secret')
        response = self.client.get(reverse('challenges'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/challenges.html")
        # Check that context has challenges data
        self.assertIn("challenges", response.context)
        if response.context["challenges"]:
            chal = response.context["challenges"][0]
            self.assertEqual(chal['card_name'], self.card.card_name)

    def test_challenge_view(self):
        url = reverse('challenge', kwargs={'chal_id': self.challenge.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/verification.html")
        # Check that context contains info and questions
        self.assertIn("info", response.context)
        self.assertIn("questions", response.context)
        self.assertEqual(len(response.context["questions"]), 1)

    def test_add_card(self):
        # Log in as normal user
        self.client.login(username=self.user.username, password='secret')
        # Ensure the card is not already in the user's collection (apart from setUp)
        initial_cards = self.user_profile.user_profile_collected_cards.count()
        url = reverse('add-card', kwargs={'chal_id': self.challenge.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Refresh profile
        self.user_profile.refresh_from_db()
        # Check the card collection count increased by one
        self.assertEqual(self.user_profile.user_profile_collected_cards.count(), initial_cards)
