from django.contrib import admin
from .models import Card, CardSet, UserProfile, Challenge

# Register your models here.
admin.site.register(Card)
admin.site.register(CardSet)
admin.site.register(UserProfile)
admin.site.register(Challenge)