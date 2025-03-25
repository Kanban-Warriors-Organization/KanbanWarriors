import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from cardgame.models import Card, UserProfile Trade


class TradeTestCase(TestCase):

    def setUp(self):
        # initialises a few users and makes a few trades between them
        self.client = Client()
        self.user1 = User.objects.create_user(username="martenfan",
                                             password="ilikemarten")
        self.user_profile1 = UserProfile.objects.create(
            user=self.user1,
            user_profile_points=50,
            user_signup_date=timezone.now()
        )

        self.user2 = User.objects.create_user(username="stoatfan",
                                             password="ilikestoat")
        self.user_profile2 = UserProfile.objects.create(
            user=self.user2,
            user_profile_points=64,
            user_signup_date=timezone.now()
        )

        self.user3 = User.objects.create_user(username="wolverinefan",
                                             password="ilikewolverine")
        self.user_profile3 = UserProfile.objects.create(
            user=self.user3,
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
        )

        self.card3 = Card.objects.create(
            card_name="Wolverine",
            card_subtitle="Subtitle",
            card_description="Desc",
        )

        # cases we need to test:
        # user makes a trade with a card they have
        # user makes a trade with a card they don't have
        # user accepts a trade that they can accept
        # user accepts a trade that they cannot accept
        # user cancels a public trade
        # user cancels a private trade
        # user makes a trade with a nonexistent user
        # outgoing trades view works fine
        # incoming trades view works fine
        # idk what else, just add to this if you think i forgot something
        # -lizard


    def test_personal_trades(self):
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now()) # incoming
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             created_date=datetime.datetime.now()) # no recip
        Trade.objects.create(offered_card=self.card1,requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user3,
                             created_date=datetime.datetime.now()) # not allowd
        Trade.objects.create(offered_card=self.card2,
                             requested_card=self.card3,
                             sender=self.user2,
                             recipient=self.user3,
                             created_date=datetime.datetime.now()) # outgoing
        Trade.objects.create(offered_card=self.card2,
                             requested_card=self.card3,
                             sender=self.user2,
                             created_date=datetime.datetime.now()) # outgoing public
        self.client.login(username="stoatfan",
                          password="ilikestoat") # this is user 2
        url = reverse("personal")
        response = self.client.get(url)
        self.assertEqual(len(response.context['outgoing']), 2)
        self.assertEqual(len(response.context['incoming']), 1)




    def test_valid_trade_cancelled(self):
        # checks that a user can cancel a trade they made
        self.client.login(username="martenfan",
                          password="ilikemarten")
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        # cancels the trade, i think
        url = reverse("cancel", kwargs={"t_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # validate that the trade is cancelled
        self.assertEqual(Trade.objects.filter(offered_card=self.card1).count(), 0)

    def test_valid_trade_cancelled_when_recipient(self):
        # tests that a user can cancel a trade that they are the recipient of
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.client.login(username="stoatfan", password="ilikestoat")
        url = reverse("cancel", kwargs={"t_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # validate that the trade is cancelled
        self.assertEqual(Trade.objects.filter(offered_card=self.card1).count(),0)

    def test_invalid_trade_not_cancelled(self):
        # checks that a user cannot cancel a trade they did not make or receive
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.client.login(username="wolverinefan",
                          password="ilikewolverine")
        url = reverse("cancel",
                      kwargs={"t_id": 1})
        self.client.get(url)
        # validate that the trade is not cancelled
        self.assertEqual(
            Trade.objects.filter(offered_card=self.card1).count(), 1)

    def test_invalid_trade_not_accepted(self):
        # tests that a user cannot accept a trade directed at a different player
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.user_profile3.user_profile_collected_cards.add(self.card2)
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.client.login(username="wolverinefan",
                          password="ilikewolverine")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        self.client.get(url, HTTP_REFERER=referee)
        # check that nothing has changed
        self.assertTrue(self.card2 in self.user_profile3
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 not in self.user_profile3
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card2 not in self.user_profile1
                        .user_profile_collected_cards.all())

    def test_accepting_targeted_trade(self):
        # tests that a player can accept a trade directed to
        # them when both players have the right cards
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.client.login(username="stoatfan", password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id":1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        #namely that user2 has card 1 and that user1 has card 2
        self.assertTrue(self.card2 in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 not in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 in self.user_profile2
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card2 not in self.user_profile2
                        .user_profile_collected_cards.all())

    def test_accepting_untargeted_trade(self):
        #tests that a player can accept a public trade when both players have the right cards

        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             created_date=datetime.datetime.now())
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id":1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        #namely that user2 has card 1 and that user1 has card 2
        self.assertTrue(self.card2 in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 not in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 in self.user_profile2
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card2 not in self.user_profile2
                        .user_profile_collected_cards.all())

    def test_accepting_trade_without_receiver_having_necessary_card(self):
        #tests that accepting a trade has no result if
        # the receipient does not have the requested card
        #user1 has card1 and user2 does not have card2
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        #user_profile2.user_profile_collected_cards.add(card2)
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.client.login(username="stoatfan",
                          password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        self.assertTrue(self.card1 not in self.user_profile2
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card2 not in self.user_profile1
                        .user_profile_collected_cards.all())

    def test_accepting_trade_without_sender_having_necessary_card(self):
        #tests that accepting a trade has no result if
        # the sender does not have the offered card
        #user1 does not have card1, and user2 has card2
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        #user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        self.assertTrue(self.card1 not in self.user_profile2
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card2 not in self.user_profile1
                        .user_profile_collected_cards.all())

    def test_accepting_when_sender_has_requested_card(self):
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.user_profile1.user_profile_collected_cards.add(self.card2)
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        self.client.login(username="stoatfan",
                          password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        response = self.client.get(url, HTTP_REFERER=referee)
        #checks the state of the database
        self.assertEqual(Trade.objects.all().count(), 1)

    def test_accepting_when_receiver_has_offered_card(self):
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user2,
                             created_date=datetime.datetime.now())
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.user_profile2.user_profile_collected_cards.add(self.card1)
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        #user_profile1.user_profile_collected_cards.add(card1)
        self.client.login(username="stoatfan",
                          password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        self.assertEqual(Trade.objects.all().count(), 1)


    def test_accepting_trade_directed_to_another_person(self):
        #tests that a user cannot accept a trade not directed towards them
        Trade.objects.create(offered_card=self.card1,
                             requested_card=self.card2,
                             sender=self.user1,
                             recipient=self.user3,
                             created_date=datetime.datetime.now())
        self.user_profile2.user_profile_collected_cards.add(self.card2)
        self.user_profile1.user_profile_collected_cards.add(self.card1)
        self.client.login(username="stoatfan",
                          password="ilikestoat")
        referee = 'http://testserver{}'.format(reverse('personal'))
        url=reverse("accept", kwargs={"t_id": 1})
        self.client.get(url, HTTP_REFERER=referee)

        #checks the state of the database
        self.assertTrue(self.card2 not in self.user_profile1
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 not in self.user_profile2
                        .user_profile_collected_cards.all())
        self.assertTrue(self.card1 in self.user_profile1
                        .user_profile_collected_cards.all())
