# import datetime
# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.utils import timezone

# #test case for various account operations accessible from the "accounts" page
# class AccountTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = create_user(username="martenfan",email="ma@rt.en", password="ilikemarten")
#         UserProfile.objects.create(user=self.user,user_profile_points=1024,user_signup_date=timezone.now())

#     def test_username_pwd_correct(self):
#         response = client.post("change_username", {"new_name"="martenfanagain","pwd"="ilikemarten"})
#         self.AssertEqual(User.objects.filter(username="martenfan").count(), 0)
#         self.AssertEqual(User.objects.filter(username="martenfanagain").count(), 1)

#     def test_username_pwd_incorrect(self):
#             response = client.post("change_username", {"new_name"="martenfanagain","pwd"="ihatemarten"})
#             self.AssertEqual(User.objects.filter(username="martenfan").count(), 1)
#             self.AssertEqual(User.objects.filter(username="martenfanagain").count(), 0)

#     def test_delete_account_pwd_correct(self):
#         response = client.post("delete_account", {"password"="ilikemarten"})
#         #check account and user profile are gone
#         self.AssertEqual(User.objects.filter(username="martenfan").count(), 0)
#         self.AssertEqual(UserProfile.objects.filter(user.username="martenfan").count(), 0)
#         pass

#     def test_delete_account_pwd_incorrect(self):
#         response = client.post("delete_account", {"password"="ihatemarten"})
#         #check account and user profile are gone
#         self.AssertEqual(User.objects.filter(username="martenfan").count(), 1)
#         self.AssertEqual(UserProfile.objects.filter(user.username="martenfan").count(), 1)
#         pass