from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def index(request):
    return HttpResponse("index page test")

def card_col(request, user_name):
    response = "you're at the collection of %s"

    #gets file names from database
    a = "number of cards: "
    try:
        u = UserProfile.objects.get(user__username=user_name) #this is a query set
        for i in u.user_profile_collected_cards.all():
            a += "s"
    except ObjectDoesNotExist:
        return HttpResponse("skibidi") #this seems to happen every time


    return HttpResponse("a")

    return HttpResponse(response % user_name)

def login(LoginView):
    pass

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid(): #validation later
            try:
                User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
                return HttpResponse("you did good!")
            except IntegrityError:
                pass
        return HttpResponse("you done goofed!")


    else:
        form = UserCreationForm()
        return HttpResponse(render(request, "cardgame/signup.html", {'form':form}))

