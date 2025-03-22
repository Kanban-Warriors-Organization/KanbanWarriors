"""
Admin configuration.

This file registers the models with the Django admin interface.

Author: BLANK
"""

from django.contrib import admin
from .models import Card, UserProfile, Challenge, Question, Trade

# Register your models here.
admin.site.register(Card)
admin.site.register(UserProfile)
admin.site.register(Challenge)
admin.site.register(Question)
admin.site.register(Trade)
