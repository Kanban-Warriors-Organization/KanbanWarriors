"""
Test suite for model validation and data integrity.
Verifies the correct functionality of data models including creation, 
attribute storage, and relationship management.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from cardgame.models import Card, CardSet, UserProfile


class CardModelTests(TestCase):
    """
    Test suite for validating model functionality.
    Ensures proper creation and storage of Card, CardSet, and UserProfile
    including their relationships and attributes.

    Author: BLANK
    """

    def test_card_created_with_correct_details(self):
        """
        Validates that a card stores and returns its creation attributes correctly.
        Tests card name, subtitle, description, and card set relationship.
        """
        # Create the test CardSet
        test_card_set_name = "Test_Card_Set_Name"
        test_card_set_description = "Test_Card_Set_Description"
        test_card_set = CardSet(card_set_name = test_card_set_name,
                                card_set_description = test_card_set_description)
        test_card_set.save()

        # Create the test Card
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_card = Card(card_name = test_card_name, card_subtitle = test_card_subtitle,
                         card_description = test_card_description, card_set = test_card_set)
        test_card.save()

        #Test card_name is the expected value
        self.assertIs(test_card.card_name, test_card_name,
                      "card_name was not set or returned correctly\n\
                      expected: " + str(test_card_name) + "\n\
                      actual:   " + str(test_card.card_name))

        #Test card_subtitle is the expected value
        self.assertIs(test_card.card_subtitle, test_card_subtitle,
                      "card_subtitle was not set or returned correctly\n\
                      expected: " + str(test_card_subtitle) + "\n\
                      actual:   " + str(test_card.card_subtitle))

        #Test card_description is the expected value
        self.assertIs(test_card.card_description, test_card_description,
                      "card_description was not set or returned correctly\n\
                      expected: " + str(test_card_description) + "\n\
                      actual:   " + str(test_card.card_description))

        #Test card_set is the expected value
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
        test_card_set = CardSet(card_set_name = test_card_set_name,
                                card_set_description = test_card_set_description)

        #Test card_set_name is the expected value
        self.assertIs(test_card_set.card_set_name, test_card_set_name,
                      "card_set_name was not set or returned correctly\n\
                      expected: " + str(test_card_set_name) + "\n\
                      actual:   " + str(test_card_set.card_set_name))

        #Test card_set_description is the expected value
        self.assertIs(test_card_set.card_set_description, test_card_set_description,
                      "card_set_name was not set or returned correctly\n\
                      expected: " + str(test_card_set_description) + "\n\
                      actual:   " + str(test_card_set.card_set_description))

        #TODO Create tests for image once implemented

    def test_user_profile_set_with_correct_details_and_links_to_user(self):
        """
        Ensures user profile creation with proper attribute storage and user linkage.
        Tests points system, card collection relationships, and user association.
        """
        # Create test User
        test_user_username = "Test_User"
        test_user_password = "Test_Password"
        test_user = User.objects.create_user(username = test_user_username,
                                             password = test_user_password)
        test_user.save()

        # Create a test Card for the collected_cards field
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_user_profile_collected_cards = Card(card_name = test_card_name,
                                                card_subtitle = test_card_subtitle,
                                                card_description = test_card_description,
                                                card_set = None)
        test_user_profile_collected_cards.save()

        # Create the actual UserProfile model
        test_user_profile_points = 100
        test_user_profile = UserProfile(user = test_user,
                                        user_profile_points = test_user_profile_points)
        test_user_profile.save()
        test_user_profile.user_profile_collected_cards.add(test_user_profile_collected_cards)

        #Test that user_profile_points are the expected value
        self.assertIs(test_user_profile.user_profile_points, test_user_profile_points,
                      "user_profile_points was not set or returned correctly\n\
                      expected: " + str(test_user_profile_points) + "\n\
                      actual:   " + str(test_user_profile.user_profile_points))

        #Test that user_profile_collected_cards is the expected value
        self.assertEqual(test_user_profile.user_profile_collected_cards.all()[0].card_name,
                      test_user_profile_collected_cards.card_name,
                      "user_profile_collected_cards was not set or returned correctly\n\
                      expected: " + str(test_user_profile_collected_cards) + "\n\
                      actual:   " + str(test_user_profile.user_profile_collected_cards.all()[0]))

        #Test that the user is the expected value
        self.assertIs(test_user_profile.user, test_user,
                      "user was not set or returned correctly\n\
                      expected: " + str(test_user) + "\n\
                      actual:   " + str(test_user_profile.user))
