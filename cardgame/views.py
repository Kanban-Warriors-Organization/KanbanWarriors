from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

# Create your views here.

def index(request):
    return HttpResponse("index page test")

def home(request):
    #we render the top scoring players, so we have to get their scores!
    users = UserProfile.objects.all().order_by('-user_profile_points').values()[:5]
    names = []
    scores = []
    for usr in users:
        up_record = UserProfile.objects.get(user_id= usr['user_id'])

        names.append(up_record.user.username)
        scores.append(up_record.user_profile_points)
    return render(request, 'cardgame/home.html', {'names': names, 'scores':scores})

def card_col(request, user_name):
    #gets the cards from a user's collection and inserts them into the template as context
    try:
        imgs = []
        u = UserProfile.objects.get(user__username=user_name)
        for i in u.user_profile_collected_cards.all():
            imgs.append(i.card_image_link) #remember, this is an in image field!
        return render(request, 'cardgame/card_col.html', {'images':imgs}) 
    
    except ObjectDoesNotExist:
        #if user does not exist
        pass
    return HttpResponse("fail") #change this later!



def login(LoginView):
    pass


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():  # validation later
            try:
                User.objects.create_user(
                    form.cleaned_data["username"], None, form.cleaned_data["password1"]
                )
                return HttpResponse("you did good!")
            except IntegrityError:
                pass
        return HttpResponse("you done goofed!")

    else:
        form = UserCreationForm()
        return HttpResponse(render(request, "cardgame/signup.html", {"form": form}))


@staff_member_required
def create_card(request):
    if request.method == "POST":  # Create a card
        # Get info from request
        card_name = request.POST.get("card_name")
        card_subtitle = request.POST.get("card_subtitle")
        card_description = request.POST.get("card_description")
        card_set_name = request.POST.get("card_set")

        # Check that the required parameters are provided
        if not (card_name and card_subtitle and card_description):
            return HttpResponse("Missing required parameters", status=400)

        # Get card set if available
        card_set_instance = None
        if card_set_name:
            try:
                card_set_instance = CardSet.objects.get(card_set_name=card_set_name)
            except CardSet.DoesNotExist:
                return HttpResponse("Specified CardSet does not exist", status=400)

        try:
            Card.objects.create(
                card_name=card_name,
                card_subtitle=card_subtitle,
                card_description=card_description,
                #TODO: add image parameter!!!!
                card_set=card_set_instance,
            )
            return HttpResponse("Card created successfully!")
        except IntegrityError as e:  # catches errors such as non-unique primary key
            return HttpResponse(f"Error creating card: {e}")
    else:  # GET: Render UI for creating a card
        return render(request, "cardgame/create_card.html")

def get_locations(request):
    locations = list(Challenge.objects.select_related("Card").values(
        "Card__card_name",  
        "lat",
        "long"
    ))

    formatted_locations = [
        {"name": loc["Card__card_name"], "latitude": loc["lat"], "longitude": loc["long"]}
        for loc in locations
    ]

    return JsonResponse({"locations": formatted_locations})

def signout(request):

    logout(request)
    redirect("home") #this is currently bugged!
    #when this is deployed in production, you HAVE to modify the htaccess file
    #so that the ".html" at the end of the URL is removed.
    #proceed with caution! -AGP-

def profile(request, user_name):

    try:
        u = UserProfile.objects.get(user__username=user_name)
        ctx = {"username": user_name} #just puts out the username at the moment
        #return render(request, "cardgame/profile.html", ctx)
        #profile.html not implemented yet!
        return HttpResponse("profile of " + user_name)

    except ObjectDoesNotExist:
        pass

    return HttpResponse("failure!")##do something more verbose

def challenge(request, challenge_id):

#we need to get the challenge, the questions, and the answers.
    try:

    except ObjectDoesNotExist:
        pass

    return HttpResponse("failure!")

