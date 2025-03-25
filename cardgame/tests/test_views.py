import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


from cardgame.models import Card, UserProfile, Challenge, Question


class EmptyTestCase(TestCase):
    """
    This is for testing on an empty database
    Namely, that the correct responses are returned if a user attempts to
    access an object that does not exist
    Written by -Adam-
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="professor y",
                                             password="secret")
        UserProfile.objects.create(
            user=self.user,
            user_profile_points=64,
            user_signup_date=timezone.now()
        )

    def test_profile_when_user_nonexistent(self):
        url = reverse("profile", kwargs={"user_name": "professor x"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cardcol_when_user_nonexistent(self):
        url = reverse("cardcollection", kwargs={"user_name": "professor x"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # *** FIX: use a valid positive challenge ID that doesn’t exist ***
    def test_challenge_that_does_not_exist(self):
        self.client.force_login(self.user)
        url = reverse("challenge", kwargs={"chal_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_with_no_cards(self):
        url = reverse("cardcollection", kwargs={"user_name": "professor y"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_challenges_when_none_available(self):
        self.client.force_login(self.user)
        url = reverse("challenges")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user and its profile
        self.user = User.objects.create_user(username="testuser",
                                             password="secret")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_profile_points=50,
            user_signup_date=timezone.now()
        )

        self.card = Card.objects.create(
            card_name="TestCard",
            card_subtitle="Subtitle",
            card_description="Desc",
        )

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
            status="ongoing",
        )
        # Create a question for challenge view
        self.question = Question.objects.create(
            challenge=self.challenge,
            text="Test question?",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_answer="B",
        )

    def test_card_col(self):
        # Test card collection view for existing user
        self.user_profile.user_profile_collected_cards.add(self.card)
        url = reverse("cardcollection",
                      kwargs={"user_name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cardshas", response.context)
        self.assertEqual(response.context["cardshas"][0]["title"], "TestCard")

    def test_card_col_404(self):
        # checks that accessing a nonexistent card collections returns a 404
        url = reverse("cardcollection",
                      kwargs={"user_name": "nonexistent_user"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recent_card_data(self):
        response = self.client.get(reverse("recent_card_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("name", json_data)
        self.assertEqual(json_data["name"], self.card.card_name)
        self.assertIn("description", json_data)
        self.assertIn("image", json_data)

    def test_signup_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/signup.html")

    def test_signup_post(self):
        signup_data = {
            "username": "newuser",
            "password1": "strongPassword123",
            "password2": "strongPassword123",
            "email": "newuser@gmail.com",
        }
        response = self.client.post(reverse("signup"), data=signup_data)
        self.assertEqual(response.status_code, 302)
        # Check that the user is created:
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Checks that another user is NOT made if the same credentials are used
        self.client.post(reverse("signup"), data=signup_data)
        self.assertTrue(User.objects.filter(username="newuser").count() == 1)

    # In test_views.py, modify your test_create_card_get_and_post method:

    def test_create_card_get_and_post(self):
        # Create staff user for creating cards
        User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

        # Ensure the background image exists in static/card_gen/back.png
        from django.conf import settings
        import os

        static_dir = os.path.join(settings.BASE_DIR, "static", "card_gen")
        os.makedirs(static_dir, exist_ok=True)
        back_img_path = os.path.join(static_dir, "back.png")
        if not os.path.exists(back_img_path):
            from PIL import Image

            img = Image.new("RGB", (100, 100), color="blue")
            img.save(back_img_path)

        # Prepare image for upload using the provided do_not_remove.png
        upload_img_path = os.path.join(
            settings.BASE_DIR, "cardgame", "media",
            "card_images", "do_not_remove.png"
        )
        with open(upload_img_path, "rb") as f:
            file_data = f.read()
        image_data = SimpleUploadedFile(
            "card_image.png", file_data, content_type="image/png"
        )

        post_data = {
            "card_name": "NewCard",
            "card_subtitle": "NewSubtitle",
            "card_description": "New description",
        }
        files_data = {"card_image": image_data}

        from PIL import Image as PilImage
        from unittest.mock import patch

        # Create a dummy image to return from make_image
        dummy_image = PilImage.new("RGB", (100, 100))

        # Patch make_image to return a dummy PIL image (with a .save method)
        with patch(
            "cardgame.views.make_image", return_value=dummy_image
        ) as mock_make_image:
            response_post = self.client.post(
                reverse("create_card"), data=post_data, files=files_data
            )
            mock_make_image.assert_called_once()

        # Check response and database creation
        self.assertEqual(response_post.status_code, 200)
        self.assertTrue(Card.objects.filter(card_name="NewCard").exists())

        # Clean up: remove the image file created by the view
        # (if it’s not the default)
        new_card = Card.objects.get(card_name="NewCard")
        if new_card.card_image_link and hasattr(new_card.card_image_link,
                                                "path"):
            file_path = new_card.card_image_link.path
            default_image_path = os.path.join(
                settings.BASE_DIR, "static", "card_images", "do_not_remove.png"
            )
            if os.path.exists(file_path) and os.path.abspath(
                file_path
            ) != os.path.abspath(default_image_path):
                os.remove(file_path)

    def test_get_locations(self):
        self.client.login(username=self.user.username, password="secret")
        response = self.client.get(reverse("locations_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("locations", json_data)
        # The challenge's card name should appear in the locations
        self.assertEqual(json_data["locations"][0]["name"],
                         self.card.card_name)

    def test_leaderboard_data(self):
        # Create additional users with points
        user2 = User.objects.create_user(username="user2", password="secret2")
        UserProfile.objects.create(
            user=user2, user_profile_points=80, user_signup_date=timezone.now()
        )
        response = self.client.get(reverse("leaderboard_data"))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIsInstance(json_data, list)
        # Check that at most 5 players are returned.
        self.assertLessEqual(len(json_data), 5)

    def test_signout(self):
        # Log in and then sign out
        self.client.login(username=self.user.username, password="secret")
        response = self.client.get(reverse("logout"))
        # After signout, it should redirect to home or return
        # a status code (our view returns HttpResponse)
        self.assertIn(response.status_code, [200, 302])

    def test_profile(self):
        url = reverse("profile", kwargs={"user_name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Since profile.html is not implemented,
        # response may be a simple HttpResponse text.
        self.assertIn(self.user.username, response.content.decode())

    def test_challenges(self):
        # Ensure user is logged in for challenges view
        self.client.login(username=self.user.username, password="secret")
        response = self.client.get(reverse("challenges"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/challenges.html")
        # Check that context has challenges data
        self.assertIn("challenges", response.context)
        if response.context["challenges"]:
            chal = response.context["challenges"][0]
            self.assertEqual(chal["card_name"], self.card.card_name)

    def test_challenge_view(self):
        self.client.login(username=self.user.username, password="secret")
        url = reverse("challenge", kwargs={"chal_id": self.challenge.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cardgame/verification.html")
        # Check that context contains info and questions
        self.assertIn("info", response.context)
        self.assertIn("questions", response.context)
        self.assertEqual(len(response.context["questions"]), 1)

    def test_add_card(self):
        # Log in as normal user
        self.client.login(username=self.user.username, password="secret")
        # Ensure the card is not already in the user's
        # collection (apart from setUp)
        initial_cards = self.user_profile.user_profile_collected_cards.count()
        url = reverse("add-card", kwargs={"chal_id": self.challenge.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Refresh profile
        self.user_profile.refresh_from_db()
        # Check the card collection count increased by one
        self.assertEqual(
            self.user_profile.user_profile_collected_cards.count(),
            initial_cards + 1
        )
