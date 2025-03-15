"""
Core data models for the application.
Defines database structure and relationships for cards, collections,
user profiles, challenges, and quiz components.

"""

import datetime
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

class CardSet(models.Model):
    """
    Represents a collection of related cards.

    Attributes:
        card_set_name (str): Unique identifier for the set
        card_set_description (str): Detailed description of the set's theme

    Relationships:
        One-to-many with Card model

    Author: Timothy Simmons
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
        environmental_friendliness (int): Battle stat for environmental impact
        beauty (int): Battle stat for aesthetic appeal
        cost (int): Battle stat for resource cost

    Relationships:
        Many-to-one with CardSet
        Many-to-many with UserProfile

    Author: Timothy Simmons
    """

    card_name = models.CharField(max_length=100, primary_key=True)
    card_subtitle = models.CharField(max_length=100)
    card_description = models.CharField(max_length=400)
    card_created_at = models.DateTimeField(auto_now_add=True)
    card_image_link = models.ImageField(
        upload_to="static/card_images",
        default="static/card_images/do_not_remove.png",
    )
    card_set = models.ForeignKey(CardSet, models.SET_NULL,
                                 null=True, blank=True)
    
    # Battle stats
    environmental_friendliness = models.IntegerField(default=0)
    beauty = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

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

    Author: Timothy Simmons
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    user_profile_points = models.IntegerField(default=0)
    user_profile_collected_cards = models.ManyToManyField(Card, blank=True)
    # potential problem if card is deleted
    user_most_recent_card = models.CharField(default="nocards", max_length=100)
    user_most_recent_card_date = models.DateField(null=True, blank=True)
    user_signup_date = models.DateField()

    @classmethod
    def create(cls, created_user):
        """
        Creation method for a new User
        """
        try:
            ctime = datetime.datetime.now()
            up = cls(user=created_user, user_signup_date=ctime)
        except Exception as e:
            print(e)
        return up


class Question(models.Model):
    """
    Faciliates the multiple-choice questions associated with a challenge

    Author: Taha-Cem Bakirhan
    """

    # Links to challenge
    challenge = models.ForeignKey(
        "Challenge", on_delete=models.CASCADE, related_name="questions"
    )

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
        """
        Ensures that the correct answer is one of the options presented
        to the user
        """

        valid_options = {self.option_a, self.option_b,
                         self.option_c, self.option_d}
        if self.correct_answer not in valid_options:
            raise ValidationError(
                "Correct answer must match one of \
                                   the options presented"
            )

    def __str__(self):
        """
        Debugging purposes
        """
        return f"{self.text} for challenge: {self.challenge.challenge_name}"


class Challenge(models.Model):
    """
    This represents the challenge events that occur on campus that
    users can attend to earn cards and points

    Author: Taha-Cem Bakirhan
    """

    # Event details
    challenge_name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # This is the physical location for the challenge
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    # Card association
    card = models.OneToOneField(
        "Card", on_delete=models.CASCADE, related_name="challenge"
    )

    # The points awarded to a player upon
    # attendance/completion of the challenge
    points_reward = models.IntegerField(default=10)

    # Event status
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("ongoing", "ongoing"),
        ("completed", "completed"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default="upcoming")

    def __str__(self):
        """
        Debugging purposes
        """
        return (
            f"{self.challenge_name} at ({self.latitude}, {self.longitude}) "
            f"with card: {self.card.card_name}"
        )

    def clean(self):
        """
        Ensures that the end time is after the start time
        """
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
                raise ValidationError(
                    f"Missing answer for question ID: \
                                      {question.id}"
                )

            # Checks if the answer is correct
            if user_answer != question.correct_answer:
                return False

        # If all the answers are right, return True
        return True


class Battle(models.Model):
    """
    Represents an active card battle between two players.
    
    Attributes:
        room_id (str): Unique identifier for the battle room
        player1/player2 (UserProfile): The two participants
        current_turn (int): Which player's turn it is (1 or 2)
        status (str): Current state of the battle
        winner (UserProfile): The winner of the battle (if completed)
        created_at (DateTimeField): When the battle was created
        
    Author: Samuel
    """
    
    room_id = models.CharField(max_length=100, unique=True)
    player1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="battles_as_player1")
    player2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
                               related_name="battles_as_player2", null=True, blank=True)
    current_turn = models.IntegerField(default=1)  # 1 for player1, 2 for player2
    
    STATUS_CHOICES = [
        ("waiting", "Waiting for Player 2"),
        ("selecting", "Selecting Cards"),
        ("ready", "Ready to Start"),
        ("in_progress", "Battle in Progress"),
        ("completed", "Battle Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
    
    winner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, 
                              related_name="battles_won", null=True, blank=True)
    player1_ready = models.BooleanField(default=False)
    player2_ready = models.BooleanField(default=False)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Battle {self.room_id}: {self.player1.user.username} vs {self.player2.user.username if self.player2 else 'Waiting'}"
        
    def both_ready(self):
        return self.player1_ready and self.player2_ready


class BattleDeck(models.Model):
    """
    Represents cards selected by a player for a battle.
    
    Attributes:
        battle (Battle): The battle this deck belongs to
        player (UserProfile): The player who owns this deck
        cards (ManyToManyField): Selected cards for the battle
        current_card_index (int): Index of the current card in play
        shuffle_seed (int): Seed for shuffling the deck
        
    Author: Samuel
    """
    
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="decks")
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="battle_decks")
    cards = models.ManyToManyField(Card, related_name="battle_decks")
    current_card_index = models.IntegerField(default=0)
    shuffle_seed = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Deck for {self.player.user.username} in battle {self.battle.room_id}"
