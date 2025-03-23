from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
import datetime

#We ran into an issue where if a superuser was created with the command line, a UserProfile object would not be created
#This causes a huge number of issues!
#This is a hacky solution but it works

@receiver(post_save , sender = User)
def makeUserProfile(sender , instance , created , **kwargs):
    if created and instance.is_superuser  :
        up = UserProfile.objects.create(user=instance,user_signup_date=datetime.datetime.now())
        up.save()

