from django.test import TestCase
from .models import Card, CardSet, UserProfile
from django.contrib.auth.models import User

class CardModelTests(TestCase):
    """
    Tests for the models Card, CardSet, UserProfile
    """
    def test_card_created_with_correct_details(self):
        """
        Card should return the same details it was created with
        """
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"

        test_card = Card(card_name = test_card_name, card_subtitle = test_card_subtitle,
                         card_description = test_card_description, card_set = None)

        self.assertIs(test_card.card_name, test_card_name,
                      "card_name was not set or returned correctly")

        self.assertIs(test_card.card_subtitle, test_card_subtitle,
                      "card_subtitle was not set or returned correctly")

        self.assertIs(test_card.card_description, test_card_description,
                      "card_description was not set or returned correctly")

    def test_card_set_with_correct_details(self):
        """
        CardSet should return the same details it was created with
        """
        test_card_set_name = "Test_Card_Set_Name"
        test_card_set_description = "Test_Card_Set_Description"

        test_card_set = CardSet(card_set_name = test_card_set_name,
                                card_set_description = test_card_set_description)

        self.assertIs(test_card_set.card_set_name, test_card_set_name,
                      "card_set_name was not set or returned correctly")

        self.assertIs(test_card_set.card_set_description, test_card_set_description,
                      "card_set_name was not set or returned correctly")

    def test_user_profile_set_with_correct_details_and_links_to_user(self):
        """
        UserDetails should return the same details it was created with and link 
        to a User
        """
        #Create test User
        test_user_username = "Test_User"
        test_user_password = "Test_Password"
        test_user = User.objects.create_user(username = test_user_username,
                                             password = test_user_password)
        test_user.save()

        #Create a test Card for the collected_cards field
        test_card_name = "Test_Card_Name"
        test_card_subtitle = "Test_Card_Subtitle"
        test_card_description = "Test_Card_Description"
        test_user_profile_collected_cards = Card(card_name = test_card_name,
                                                card_subtitle = test_card_subtitle,
                                                card_description = test_card_description,
                                                card_set = None)
        test_user_profile_collected_cards.save()

        #Create the actual UserProfile model
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

        self.assertIs(test_user_profile.user, test_user,
                      "user was not set or returned correctly")
        
