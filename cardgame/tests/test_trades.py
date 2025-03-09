import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


from cardgame.models import Card, CardSet, UserProfile, Challenge, Question, Trade

class T(TestCase):

    def setUp(self):
       
# what we need to test:
#player accepts trade when they don't have the card
#player accepts trade, but opponent doesn't have the card

