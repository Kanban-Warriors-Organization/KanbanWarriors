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
    

