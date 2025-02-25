"""
Test suite for model validation and data integrity.
Verifies the correct functionality of data models including creation,
attribute storage, and relationship management.
"""

from datetime import timedelta
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from cardgame.models import Card, CardSet, UserProfile, Question, Challenge


class CardModelTests(TestCase):
    """
    Test suite for validating model functionality.
    Ensures proper creation and storage of Card, CardSet, and UserProfile
    including their relationships and attributes.

    Author: Timothy Simmons
    """

    def test_card_created_with_correct_details(self):
        """
        Validates that a card stores and returns its creation
        attributes correctly.
        Tests card name, subtitle, description, and card set relationship.
        """
        # Create the test CardSet
        test_card_set_name = "Test_Card_Set_Name"
        test_card_set_description = "Test_Card_Set_Description"
        test_card_set = CardSet(card_set_name=test_card_set_name,
                                card_set_description=test_card_set_description)
        test_card_set.save()

        # Create the test Card
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_card = Card(card_name=test_card_name,
                         card_subtitle=test_card_subtitle,
                         card_description=test_card_description,
                         card_set=test_card_set)
        test_card.save()

        # Test card_name is the expected value
        self.assertIs(test_card.card_name, test_card_name,
                      "card_name was not set or returned correctly\n\
                      expected: " + str(test_card_name) + "\n\
                      actual:   " + str(test_card.card_name))

        # Test card_subtitle is the expected value
        self.assertIs(test_card.card_subtitle, test_card_subtitle,
                      "card_subtitle was not set or returned correctly\n\
                      expected: " + str(test_card_subtitle) + "\n\
                      actual:   " + str(test_card.card_subtitle))

        # Test card_description is the expected value
        self.assertIs(test_card.card_description, test_card_description,
                      "card_description was not set or returned correctly\n\
                      expected: " + str(test_card_description) + "\n\
                      actual:   " + str(test_card.card_description))

        # Test card_set is the expected value
        self.assertIs(test_card.card_set, test_card_set,
                      "card_set was not set or returned correctly\n\
                      expected: " + str(test_card_set) + "\n\
                      actual:   " + str(test_card.card_set))

    def test_card_set_with_correct_details(self):
        """
        Verifies that a card set maintains accurate attribute storage.
        Tests card set name and description fields.
        """
        # Create the test CardSet
        test_card_set_name = "Test_Card_Set_Name"
        test_card_set_description = "Test_Card_Set_Description"
        test_card_set = CardSet(card_set_name=test_card_set_name,
                                card_set_description=test_card_set_description)

        # Test card_set_name is the expected value
        self.assertIs(test_card_set.card_set_name, test_card_set_name,
                      "card_set_name was not set or returned correctly\n\
                      expected: " + str(test_card_set_name) + "\n\
                      actual:   " + str(test_card_set.card_set_name))

        # Test card_set_description is the expected value
        self.assertIs(test_card_set.card_set_description,
                      test_card_set_description,
                      "card_set_name was not set or returned correctly\n\
                      expected: " + str(test_card_set_description) + "\n\
                      actual:   " + str(test_card_set.card_set_description))

        # TODO Create tests for image once implemented

    def test_user_profile_set_with_correct_details_and_links_to_user(self):
        """
        Ensures user profile creation with proper attribute
        storage and user linkage.
        Tests points system, card collection relationships,
        and user association.
        """
        # Create test User
        test_user_username = "Test_User"
        test_user_password = "Test_Password"
        test_user = User.objects.create_user(username=test_user_username,
                                             password=test_user_password)
        test_user.save()

        # Create a test Card for the collected_cards field
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_user_profile_collected_cards = Card(
            card_name=test_card_name,
            card_subtitle=test_card_subtitle,
            card_description=test_card_description,
            card_set=None)
        test_user_profile_collected_cards.save()

        # Create the actual UserProfile model
        test_user_profile_points = 100
        test_user_profile = UserProfile(
            user=test_user,
            user_profile_points=test_user_profile_points,
            user_signup_date=timezone.now())
        test_user_profile.save()
        test_user_profile.user_profile_collected_cards.add(
            test_user_profile_collected_cards)

        # Test that user_profile_points are the expected value
        self.assertIs(
            test_user_profile.user_profile_points,
            test_user_profile_points,
            "user_profile_points was not set or returned correctly\n\
            expected: " + str(test_user_profile_points) + "\n\
            actual:   " + str(test_user_profile.user_profile_points))

        # Test that user_profile_collected_cards is the expected value
        self.assertEqual(
            test_user_profile.user_profile_collected_cards.all()[0].card_name,
            test_user_profile_collected_cards.card_name,
            "user_profile_collected_cards was not set or returned correctly\n\
            expected: " + str(test_user_profile_collected_cards) + "\n\
            actual:   " +
            str(test_user_profile.user_profile_collected_cards.all()[0]))

        # Test that the user is the expected value
        self.assertIs(
            test_user_profile.user, test_user,
            "user was not set or returned correctly\n\
            expected: " + str(test_user) + "\n\
            actual:   " + str(test_user_profile.user))

    def test_question_set_with_correct_details_and_clean_works(self):
        """
        Ensure the Question model set with correct
        details and links to Challenge

        Also checks that the clean method works correctly
        """

        # Create the test Card
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_card = Card(card_name=test_card_name,
                         card_subtitle=test_card_subtitle,
                         card_description=test_card_description,
                         card_set=None)
        test_card.save()

        # Create test challenge
        test_challenge_name = "Test_Challenge_Name"
        test_challenge_description = "Test_Challenge_Description"
        test_challenge_start_time = timezone.now()
        test_challenge_end_time = timezone.now() + timedelta(days=1)
        test_challenge_longitude = 1.0
        test_challenge_latitude = -1.0
        test_challenge_points_reward = 5
        test_challenge_status = "ongoing"

        test_challenge = Challenge(
            challenge_name=test_challenge_name,
            description=test_challenge_description,
            start_time=test_challenge_start_time,
            end_time=test_challenge_end_time,
            longitude=test_challenge_longitude,
            latitude=test_challenge_latitude,
            card=test_card,
            points_reward=test_challenge_points_reward,
            status=test_challenge_status
        )
        test_challenge.save()

        # Create test question
        test_question_text = "Test_Question_Text"
        test_question_option_a = "Test_Question_Option_A"
        test_question_option_b = "Test_Question_Option_B"
        test_question_option_c = "Test_Question_Option_C"
        test_question_option_d = "Test_Question_Option_D"
        test_question_correct_answer = test_question_option_b

        test_question = Question(
            challenge=test_challenge,
            text=test_question_text,
            option_a=test_question_option_a,
            option_b=test_question_option_b,
            option_c=test_question_option_c,
            option_d=test_question_option_d,
            correct_answer=test_question_correct_answer,
        )
        test_question.save()

        # Test that text is set correctly
        self.assertEqual(
            Question.objects.all()[0].text,
            test_question_text,
            "text was not set or returned correctly\n\
            expected: " + str(test_question_text) + "\n\
            actual:   " + str(Question.objects.all()[0].text)
        )

        # Test that option_a is set correctly
        self.assertEqual(
            Question.objects.all()[0].option_a,
            test_question_option_a,
            "option_a was not set or returned correctly\n\
            expected: " + str(test_question_option_a) + "\n\
            actual:   " + str(Question.objects.all()[0].option_a)
        )

        # Test that option_b is set correctly
        self.assertEqual(
            Question.objects.all()[0].option_b,
            test_question_option_b,
            "option_b was not set or returned correctly\n\
            expected: " + str(test_question_option_b) + "\n\
            actual:   " + str(Question.objects.all()[0].option_b)
        )

        # Test that option_c is set correctly
        self.assertEqual(
            Question.objects.all()[0].option_c,
            test_question_option_c,
            "option_c was not set or returned correctly\n\
            expected: " + str(test_question_option_c) + "\n\
            actual:   " + str(Question.objects.all()[0].option_c)
        )

        # Test that option_d is set correctly
        self.assertEqual(
            Question.objects.all()[0].option_d,
            test_question_option_d,
            "option_d was not set or returned correctly\n\
            expected: " + str(test_question_option_d) + "\n\
            actual:   " + str(Question.objects.all()[0].option_d)
        )

        # Test that correct_answer is set correctly
        self.assertEqual(
            Question.objects.all()[0].correct_answer,
            test_question_correct_answer,
            "correct_anwser was not set or returned correctly\n\
            expected: " + str(test_question_correct_answer) + "\n\
            actual:   " + str(Question.objects.all()[0].correct_answer)
        )

        # Test that challenge is set correctly
        self.assertEqual(
            Question.objects.all()[0].challenge,
            test_challenge,
            "challenge was not set or returned correctly\n\
            expected: " + str(test_challenge) + "\n\
            actual:   " + str(Question.objects.all()[0].challenge)
        )

        # Test that .clean() doesn't fail
        Question.objects.all()[0].clean()

        # Change question correct answer so .clean() will fail
        q = Question.objects.all()[0]
        q.correct_answer = "Incorrect_Answer"
        q.save()

        with self.assertRaises(ValidationError):
            Question.objects.all()[0].clean()

    def test_challenge_set_with_correct_details_and_clean_works(self):
        """
        Ensures the Challenge model set with the correct
        details

        Also checks that the clean method works correctly
        """

        # Create the test Card
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_card = Card(card_name=test_card_name,
                         card_subtitle=test_card_subtitle,
                         card_description=test_card_description,
                         card_set=None)
        test_card.save()

        # Create test challenge
        test_challenge_name = "Test_Challenge_Name"
        test_challenge_description = "Test_Challenge_Description"
        test_challenge_start_time = timezone.now()
        test_challenge_end_time = timezone.now() + timedelta(days=1)
        test_challenge_longitude = 1.0
        test_challenge_latitude = -1.0
        test_challenge_points_reward = 5
        test_challenge_status = "ongoing"

        test_challenge = Challenge(
            challenge_name=test_challenge_name,
            description=test_challenge_description,
            start_time=test_challenge_start_time,
            end_time=test_challenge_end_time,
            longitude=test_challenge_longitude,
            latitude=test_challenge_latitude,
            card=test_card,
            points_reward=test_challenge_points_reward,
            status=test_challenge_status
        )
        test_challenge.save()

        # Test that challenge_name is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].challenge_name,
            test_challenge_name,
            "challenge_name was not set or returned correctly\n\
            expected: " + str(test_challenge_name) + "\n\
            actual:   " + str(Challenge.objects.all()[0].challenge_name)
        )

        # Test that description is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].description,
            test_challenge_description,
            "description was not set or returned correctly\n\
            expected: " + str(test_challenge_description) + "\n\
            actual:   " + str(Challenge.objects.all()[0].description)
        )

        # Test that start_time is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].start_time,
            test_challenge_start_time,
            "start_time was not set or returned correctly\n\
            expected: " + str(test_challenge_start_time) + "\n\
            actual:   " + str(Challenge.objects.all()[0].start_time)
        )

        # Test that end_time is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].end_time,
            test_challenge_end_time,
            "end_time was not set or returned correctly\n\
            expected: " + str(test_challenge_end_time) + "\n\
            actual:   " + str(Challenge.objects.all()[0].end_time)
        )

        # Test that longitude is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].longitude,
            test_challenge_longitude,
            "longitude was not set or returned correctly\n\
            expected: " + str(test_challenge_longitude) + "\n\
            actual:   " + str(Challenge.objects.all()[0].longitude)
        )

        # Test that latitude is set correctly
        self.assertEqual(
            Challenge.objects.all()[0].latitude,
            test_challenge_latitude,
            "latitude was not set or returned correctly\n\
            expected: " + str(test_challenge_latitude) + "\n\
            actual:   " + str(Challenge.objects.all()[0].latitude)
        )

        # Test that card is the expected value
        self.assertEqual(
            Challenge.objects.all()[0].card.card_name,
            test_card.card_name,
            "card was not set or returned correctly\n\
            expected: " + str(test_card.card_name) + "\n\
            actual:   " + str(Challenge.objects.all()[0].card.card_name))

        self.assertEqual(
            Challenge.objects.all()[0].points_reward,
            test_challenge_points_reward,
            "points_reward was not set or returned correctly\n\
            expected: " + str(test_challenge_points_reward) + "\n\
            actual:   " + str(Challenge.objects.all()[0].points_reward)
        )

        self.assertEqual(
            Challenge.objects.all()[0].status,
            test_challenge_status,
            "status was not set or returned correctly\n\
            expected: " + str(test_challenge_status) + "\n\
            actual:   " + str(Challenge.objects.all()[0].status)
        )

        # Test that .clean() doesn't fail
        Challenge.objects.all()[0].clean()

        # Change question correct answer so .clean() will fail
        c = Challenge.objects.all()[0]
        c.end_time = timezone.now() - timedelta(days=2)
        c.save()

        with self.assertRaises(ValidationError):
            Challenge.objects.all()[0].clean()

        # TODO implement tests for validate answers
