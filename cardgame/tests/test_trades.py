import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


from cardgame.models import Card, CardSet, UserProfile, Challenge, Question, Trade


class TradeTestCase(TestCase):

    def setUp(self):
        #initialises a few users and makes a few trades between them
        self.client = Client()
        self.user = create_user(username="martenfan",
                                             password="ilikemarten")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_profile_points=50,
            user_signup_date=timezone.now()
        )

        self.user2 = create_user(username="stoatfan",
                                             password="ilikestoat")
        self.user_profile2 = UserProfile.objects.create(
            user=self.user,
            user_profile_points=64,
            user_signup_date=timezone.now()
        )

        self.user3 = create_user(username="wolverinefan",
                                             password="ilikewolverine")
        self.user_profile3 = UserProfile.objects.create(
            user=self.user,
            user_profile_points=78,
            user_signup_date=timezone.now()
        )

        self.card = Card.objects.create(
            card_name="Stoat",
            card_subtitle="Subtitle",
            card_description="Desc",
        )

        self.card2 = Card.objects.create(
            card_name="Marten",
            card_subtitle="Subtitle",
            card_description="Desc",
            card_set=self.card_set,
        )

        self.card3 = Card.objects.create(
            card_name="Wolverine",
            card_subtitle="Subtitle",
            card_description="Desc",
            card_set=self.card_set,
        )

        #cases we need to test:
        #user makes a trade with a card they have
        #user makes a trade with a card they don't have
        #user accepts a trade that they can accept
        #user accepts a trade that they cannot accept
        #user cancels a public trade
        #user cancels a private trade
        #user makes a trade with a nonexistent user
        #outgoing trades view works fine
        #incoming trades view works fine
        #idk what else, just add to this if you think i forgot something
        #-lizard










