"""
Core data models for the application.
Defines database structure and relationships for cards, collections,
user profiles, challenges, and quiz components.

Author: BLANK
"""

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class CardSet(models.Model):
    """
    Represents a collection of related cards.

    Attributes:
        card_set_name (str): Unique identifier for the set
        card_set_description (str): Detailed description of the set's theme

    Relationships:
        One-to-many with Card model
    """

    card_set_name = models.CharField(max_length=40, primary_key=True)
    card_set_description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.card_set_name)


class Card(models.Model):
    """
    Represents an individual collectible card.

    Attributes:
        card_name (str): Unique identifier for the card
        card_subtitle (str): Secondary descriptive text
        card_description (str): Detailed card information
        card_image_link (ImageField): Visual representation

    Relationships:
        Many-to-one with CardSet
        Many-to-many with UserProfile
    """

    card_name = models.CharField(max_length=50, primary_key=True)
    card_subtitle = models.CharField(max_length=50)
    card_description = models.CharField(max_length=400)
    card_image_link = models.ImageField(
        upload_to="cardgame/static/card_images",
        default="static/card_images/do_not_remove.png",
    )
    card_set = models.ForeignKey(CardSet, models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return str(self.card_name)


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional functionality.

    Attributes:
        user_profile_points (int): Achievement score
        user_profile_collected_cards (ManyToManyField): Collection of cards

    Relationships:
        One-to-one with Django User model
        Many-to-many with Card
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    user_profile_points = models.IntegerField(default=0)
    user_profile_collected_cards = models.ManyToManyField(Card)


class Challenge(models.Model):
    """
    Represents a location-based interactive challenge.

    Attributes:
        long (float): Longitude coordinate
        lat (float): Latitude coordinate
        start (DateTime): Challenge start time
        end (DateTime): Challenge end time

    Relationships:
        One-to-one with Card
    """

    long = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # new
    # add questions later!
    Card = models.OneToOneField(Card, on_delete=models.CASCADE,
                                primary_key=False)


class Question(models.Model):
    """
    Represents a quiz question within a challenge.

    Attributes:
        text (str): Question content

    Relationships:
        Many-to-one with Challenge
    """

    text = models.CharField(max_length=400)
    challenge = models.ForeignKey(Challenge, models.SET_NULL,
                                  null=True, blank=True)


class Answer(models.Model):
    """
    Represents a possible answer to a quiz question.

    Attributes:
        text (str): Answer content
        correct (bool): Indicates if this is the correct answer

    Relationships:
        Many-to-one with Question
    """

    question = models.ForeignKey(Question, models.SET_NULL,
                                 null=True, blank=True)
    text = models.CharField(max_length=400)
    correct = models.BooleanField()
