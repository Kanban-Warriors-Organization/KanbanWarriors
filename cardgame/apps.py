"""
Application configuration.

This module defines the configuration for the cardgame Django app.

Author: BLANK
"""

from django.apps import AppConfig


class CardgameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cardgame"

    def ready(self):
        import cardgame.signals
