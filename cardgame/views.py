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
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

# Create your views here.


def index(request):
    return HttpResponse("index page test")

def home(request):
    return render(request, 'home.html')

def card_col(request, user_name):
    response = "you're at the collection of %s"

    # gets file names from database
    a = "number of cards: "
    try:
        u = UserProfile.objects.get(user__username=user_name)  # this is a query set
        for i in u.user_profile_collected_cards.all():
            a += "s"
    except ObjectDoesNotExist:
        return HttpResponse("skibidi")  # this seems to happen every time

    return HttpResponse("a")

    return HttpResponse(response % user_name)


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