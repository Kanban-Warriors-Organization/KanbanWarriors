import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from cardgame.models import Card, UserProfile, Challenge, Question, Trade


#test case for various account operations accessible from the "accounts" page
class AccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="martenfan",email="ma@rt.en", password="ilikemarten")
        UserProfile.objects.create(user=self.user1,user_profile_points=1024,user_signup_date=timezone.now())

    def test_username_pwd_correct(self):
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_username", {"new_name":"martenfanagain","pwd":"ilikemarten"})
        self.assertEqual(User.objects.filter(username="martenfan").count(), 0)
        self.assertEqual(User.objects.filter(username="martenfanagain").count(), 1)

    def test_username_pwd_incorrect(self):
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_username", {"new_name":"martenfanagain","pwd":"ihatemarten"})
        self.assertEqual(User.objects.filter(username="martenfan").count(), 1)
        self.assertEqual(User.objects.filter(username="martenfanagain").count(), 0)
    def test_delete_account_pwd_correct(self):
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/delete_account", {"pwd":"ilikemarten"})
        #check account and user profile are gone
        self.assertEqual(User.objects.filter(username="martenfan").count(), 0)
        pass

    def test_delete_account_pwd_incorrect(self):
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/delete_account", {"pwd":"ihatemarten"})
        #check account and user profile are gone
        self.assertEqual(User.objects.filter(username="martenfan").count(), 1)

        pass


