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
        self.user1 = create_user(username="martenfan",
                                             password="ilikemarten")
        self.user_profile1 = UserProfile.objects.create(
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

        self.card1 = Card.objects.create(
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





    def test_trade_404(self):
        # checks that accessing a nonexistent trade returns a 404
        url = reverse("trade",
                      kwargs={"t_id": "9001"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_valid_trade_cancelled(self):
        #checks that a user can cancel a trade they made
        self.client.login(username="martenfan",password="ilikemarten")
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        #cancels the trade, i think
        url = reverse("cancel_trade",kwargs={"t_id": 1})
        response = self.client.get(url)
        self.AssertEqual(response.status_code,200)
        #validate that the trade is cancelled
        self.AssertEqual(Trade.objects.filter(offered_card=card).count() == 0)

    def test_valid_trade_cancelled_when_recipient(self):
        #tests that a user can cancel a trade that they are the recipient of
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        self.client.login(username="stoatfan",password="ilikestoat")
        url = reverse("cancel_trade",kwargs={"t_id": 1})
        response = self.client.get(url)
        self.AssertEqual(response.status_code,200)
        #validate that the trade is cancelled
        self.AssertEqual(Trade.objects.filter(offered_card=card).count() == 0)

    def test_invalid_trade_not_cancelled(self):
        #checks that a user cannot cancel a trade they did not make or receive
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        self.client.login(username="wolverinefan",password="ilikewolverine")
        url = reverse("cancel_trade",kwargs={"t_id": 1})
        response = self.client.get(url)
        #validate that the trade is not cancelled
        self.AssertEqual(Trade.objects.filter(offered_card=card).count() == 1)

    def test_accepting_targeted_trade(self):
        #tests that a player can accept a trade directed to them when both players have the right cards
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        user_profile2.user_profile_collected_cards.add(card2)
        user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        url=reverse("accept_trade", kwargs={"t_id":1})
        response = self.client.get(url)
        #checks the state of the database
        #namely that user2 has card 1 and that user1 has card 2
        self.AssertTrue(card2 in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 not in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card2 not in user_profile2.user_profile_collected_cards.all())

    def test_accepting_untargeted_trade(self):
        #tests that a player can accept a public trade when both players have the right cards

        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,created_date=datetime.datetime.now())
        user_profile2.user_profile_collected_cards.add(card2)
        user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        url=reverse("accept_trade", kwargs={"t_id":1})
        response = self.client.get(url)
        #checks the state of the database
        #namely that user2 has card 1 and that user1 has card 2
        self.AssertTrue(card2 in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 not in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card2 not in user_profile2.user_profile_collected_cards.all())

    def test_accepting_trade_without_receiver_having_necessary_card(self):
        #tests that accepting a trade has no result if the receipient does not have the requested card
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        #user_profile2.user_profile_collected_cards.add(card2)
        user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        url=reverse("accept_trade", kwargs={"t_id":1})
        response = self.client.get(url)
        #checks the state of the database
        self.AssertTrue(card1 not in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card2 not in user_profile2.user_profile_collected_cards.all())

    def test_accepting_trade_without_sender_having_necessary_card(self):
        #tests that accepting a trade has no result if the sender does not have the offered card
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user2,created_date=datetime.datetime.now())
        user_profile2.user_profile_collected_cards.add(card2)
        #user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        url=reverse("accept_trade", kwargs={"t_id":1})
        response = self.client.get(url)
        #checks the state of the database
        self.AssertTrue(card2 not in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 not in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card2 in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card1 in user_profile1.user_profile_collected_cards.all())

    def test_accepting_trade_directed_to_another_person(self):
        #tests that a user cannot accept a trade not directed towards them
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user3,created_date=datetime.datetime.now())
        user_profile2.user_profile_collected_cards.add(card2)
        user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        url=reverse("accept_trade", kwargs={"t_id":1})

        response = self.client.get(url)
        #checks the state of the database
        self.AssertTrue(card2 not in user_profile1.user_profile_collected_cards.all())
        self.AssertTrue(card1 not in user_profile2.user_profile_collected_cards.all())
        self.AssertTrue(card1 in user_profile1.user_profile_collected_cards.all())




    def test_searching_trades(self):
        #create some trades for us to look at
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,created_date=datetime.datetime.now())
        Trade.objects.create(offered_card=card1,requested_card=card2,sender=user1,recipient=user3,created_date=datetime.datetime.now())
        Trade.objects.create(offered_card=card2,requested_card=card3,sender=user2,created_date=datetime.datetime.now())
        Trade.objects.create(offered_card=card2,requested_card=card3,sender=user1,created_date=datetime.datetime.now())
        self.client.login(username="wolverinefan",password="ilikewolverine")
        url=client.get("search_results", {"out_card"="", "in_card"=""})
        pass #i'll finish this tomorrow -l-


    #JAKE PLEASE CAN YOU WRITE TESTS FOR THE "make_trade" STUFF
    #THANK YOU


    #i will now do the page which handles getting incoming/outgoing trades


  



