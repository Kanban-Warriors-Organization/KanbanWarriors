from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, post_init
from django.contrib.auth.models import User
from .models import UserProfile, Card
import os
import datetime
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from image_gen import make_image


#We ran into an issue where if a superuser was created with the command line, a UserProfile object would not be created
#This causes a huge number of issues!
#This is a hacky solution but it works

@receiver(post_save,sender=User)
def make_admin_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser  :
        up = UserProfile.objects.create(user=instance,user_signup_date=datetime.datetime.now())
        up.save()

@receiver(post_delete,sender=Card)
def remove_card_image_after_deletion(sender, instance, using, **kwargs):
    try:
        print(str(instance.card_image_link))
        os.remove(str(instance.card_image_link))
    except Exception as e:
        pass


  
