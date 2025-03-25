from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from cardgame.models import UserProfile


# test case for various account operations accessible from the "accounts" page
class AccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="martenfan",
                                              email="ma@rt.en",
                                              password="ilikemarten")
        UserProfile.objects.create(user=self.user1,
                                   user_profile_points=1024,
                                   user_signup_date=timezone.now())

    def test_username_pwd_correct(self):
<<<<<<< HEAD
        #checks that a user can change their username
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_username", {"new_name":"martenfanagain","pwd":"ilikemarten"})
        self.assertEqual(User.objects.filter(username="martenfan").count(), 0)
        self.assertEqual(User.objects.filter(username="martenfanagain").count(), 1)

    def test_username_pwd_incorrect(self):
        #tests the password validation on the change_username view
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_username", {"new_name":"martenfanagain","pwd":"ihatemarten"})
        self.assertEqual(User.objects.filter(username="martenfan").count(), 1)
        self.assertEqual(User.objects.filter(username="martenfanagain").count(), 0)

    def test_delete_account_pwd_correct(self):
        #tests that a user can delete their account
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/delete_account", {"pwd":"ilikemarten"})
        #check account and user profile are gone
        self.assertEqual(User.objects.filter(username="martenfan").count(), 0)

    def test_delete_account_pwd_incorrect(self):
        #tests the password validation on the delete_account view
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/delete_account", {"pwd":"ihatemarten"})
        #check account and user profile are gone
=======
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/change_username",
                         {"new_name": "martenfanagain",
                          "pwd": "ilikemarten"})
        self.assertEqual(
            User.objects.filter(username="martenfan").count(), 0)
        self.assertEqual(
            User.objects.filter(username="martenfanagain").count(), 1)

    def test_username_pwd_incorrect(self):
        self.client.login(username="martenfan",
                          password="ilikemarten")
        self.client.post("/change_username",
                         {"new_name": "martenfanagain",
                          "pwd": "ihatemarten"})
        self.assertEqual(
            User.objects.filter(username="martenfan").count(), 1)
        self.assertEqual(
            User.objects.filter(username="martenfanagain").count(), 0)

    def test_delete_account_pwd_correct(self):
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/delete_account", {"pwd": "ilikemarten"})
        # check account and user profile are gone
        self.assertEqual(User.objects.filter(username="martenfan").count(), 0)

    def test_delete_account_pwd_incorrect(self):
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/delete_account", {"pwd": "ihatemarten"})
        # check account and user profile are gone
>>>>>>> ec473764392aef08fb289a328853cd5ccfcaaeb8
        self.assertEqual(User.objects.filter(username="martenfan").count(), 1)

    # fields for password change form:
    # ["old_password", "new_password1", "new_password2"]
    def test_password_valid(self):
<<<<<<< HEAD
        #tests that the change_password view works
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_password", {"old_password":"ilikemarten","new_password1":"Gulo9ine", "new_password2":"Gulo9ine"})
        self.assertTrue(authenticate(username="martenfan",password="Gulo9ine") != None)


    def test_password_mismatch(self):
        #tests that the change_password view rejects mismatched passwords
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_password", {"old_password":"ilikemarten","new_password1":"Gulo9ine", "new_password2":"Gulonine"})
        self.assertTrue(authenticate(username="martenfan",password="Gulo9ine") == None)

    def test_password_too_short(self):
        #tests that the change_password view rejects passwords that are too short
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_password", {"old_password":"ilikemarten","new_password1":"Gulo", "new_password2":"Gulo"})
        self.assertTrue(authenticate(username="martenfan",password="Gulo9ine") == None)

    def test_password_same_as_before(self):
        #tests that the change_password view rejects a password that is the same as before
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_password", {"old_password":"ilikemarten","new_password1":"ilikemarten", "new_password2":"ilikemarten"})
        self.assertTrue(authenticate(username="martenfan",password="Gulo9ine") == None)

    def test_password_old_pwd_invalid(self):
        #tests that the change_password view does not work when the old password is incorrect
        self.client.login(username="martenfan",password="ilikemarten")
        response = self.client.post("/change_password", {"old_password":"gulogulo","new_password1":"Gulo9ine", "new_password2":"Gulo9ine"})
        self.assertTrue(authenticate(username="martenfan",password="Gulo9ine") == None)



=======
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/change_password",
                         {"old_password": "ilikemarten",
                          "new_password1": "Gulo9ine",
                          "new_password2": "Gulo9ine"})
        self.assertTrue(
            authenticate(username="martenfan",
                         password="Gulo9ine") is not None)

    def test_password_mismatch(self):
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/change_password",
                         {"old_password": "ilikemarten",
                          "new_password1": "Gulo9ine",
                          "new_password2": "Gulonine"})
        self.assertTrue(
            authenticate(username="martenfan",
                         password="Gulo9ine") is None)

    def test_password_too_short(self):
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/change_password",
                         {"old_password": "ilikemarten",
                          "new_password1": "Gulo",
                          "new_password2": "Gulo"})
        self.assertTrue(
            authenticate(username="martenfan",
                         password="Gulo9ine") is None)

    def test_password_same_as_before(self):
        self.client.login(username="martenfan", password="ilikemarten")
        self.client.post("/change_password",
                         {"old_password": "ilikemarten",
                          "new_password1": "ilikemarten",
                          "new_password2": "ilikemarten"})
        self.assertTrue(
            authenticate(username="martenfan",
                         password="Gulo9ine") is None)

    def test_password_old_pwd_invalid(self):
        self.client.login(username="martenfan",
                          password="ilikemarten")
        self.client.post("/change_password",
                         {"old_password": "gulogulo",
                          "new_password1": "Gulo9ine",
                          "new_password2": "Gulo9ine"})
        self.assertTrue(
            authenticate(username="martenfan",
                         password="Gulo9ine") is None)
>>>>>>> ec473764392aef08fb289a328853cd5ccfcaaeb8
