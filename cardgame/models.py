"""
Module storing the models for the WebApp\n
Contains Card, CardSet, and UserProfile
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

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

class Question(models.Model):
    """
    Faciliates the multiple-choice questions associated with a challenge
    """

    # Links to challenge
    challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE, related_name='questions')

    # Question text
    text = models.CharField(max_length=255)

    # Multiple-choice options
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    # Correct answer should match one of the options above
    correct_answer = models.CharField(max_length=255)

    def clean(self):
        """Ensures that the correct answer is one of the options presented
        to the user"""

        valid_options = {self.option_a, self.option_b, self.option_c, self.option_d}
        if self.correct_answer not in valid_options:
            raise ValidationError("Correct answer must match one of the options presented")

    def __str__(self):
        """Debugging purposes"""
        return f"{self.text} for challenge: {self.challenge.challenge_name}"

class Challenge(models.Model):
    """
    This represents the challenge events that occur on campus that
    users can attend to earn cards and points
    """

    # Event details
    challenge_name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # This is the physical location for the challenge
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    # Card association
    card = models.OneToOneField('Card', on_delete=models.CASCADE, related_name='challenge')

    # The points awarded to a player upon attendance/completion of the challenge
    points_reward = models.IntegerField(default=10)

    # Event status
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'ongoing'),
        ('completed', 'completed')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        """Debugging purposes"""
        return (
            f"{self.challenge_name} at ({self.latitude}, {self.longitude}) "
            f"with card: {self.card.card_name}"
        )

    def clean(self):
        """Ensures that the end time is after the start time"""
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after the start time")

    def validate_answers(self, user_answers):
        """
        Validates the user's answers against the correct answers
        """
        questions = self.questions.all()
        if not questions.exists():
            raise ValidationError("No questions defined for this challenge")

        # Ensures all questions are answered
        if len(user_answers) != questions.count():
            raise ValidationError("All questions must be answered")

        # Validates each answer
        for question in questions:

            # Gets the user's answer for this question
            user_answer = user_answers.get(str(question.id))

            # Checks if the question ID exists in user_answers
            if user_answer is None:
                raise ValidationError(f"Missing answer for question ID: {question.id}")

            # Checks if the answer is correct
            if user_answer != question.correct_answer:
                return False

        # If all the answers are right, return True
        return True

    def update_status(self):
        """Updates and saves the event status based on the current time"""
        current_time = now()

        if current_time < self.start_time:
            self.status = 'upcoming'
        elif self.start_time <= current_time <= self.end_time:
            self.status = 'ongoing'
        else:
            self.status = 'completed'

        self.save()
