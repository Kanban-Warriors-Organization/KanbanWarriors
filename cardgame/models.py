"""
Module storing the models for the WebApp\n
Contains Card, CardSet, and UserProfile
"""
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class CardSet(models.Model):
    """
    Identifies a set of cards, foreign key is held in Card
    one->many relationship with cards
    """
    card_set_name = models.CharField(max_length=40, primary_key=True)
    card_set_description = models.CharField(max_length=200)
    def __str__(self):
        return str(self.card_set_name)

class Card(models.Model):
    """
    CharField: card_name\n
    CharField: card_subtitle\n
    CharField: card_description\n
    FK: card_set\n
    Holds the details of a card, can be a member of a CardSet\n
    many->one relationship with CardSet\n
    many->many relationship with UserProfile
    """
    card_name = models.CharField(max_length=50, primary_key=True)
    card_subtitle = models.CharField(max_length=50)
    card_description = models.CharField(max_length=400)
    #card_image_link = models.FieldFile() TODO Figure out how to store images
    card_set = models.ForeignKey(CardSet, models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.card_name)

class UserProfile(models.Model):
    """
    Extends the fields of the in-built User relation
    many->many relationship with Card
    one->one relationship with User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_profile_points = models.IntegerField(default=0)
    user_profile_collected_cards = models.ManyToManyField(Card)

    #for reference: django's "User" model has field "username" for the username

class Challenge(models.Model):
    long = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    start = models.DateTimeField()
    end = models.DateTimeField()
    #add questions later!
    Card = models.OneToOneField(Card, on_delete=models.CASCADE, primary_key=False)
