"""
Core functionality for user interactions, authentication, and data management.
Handles routing and processing for user profiles, card collections, challenges,
and administrative functions.
"""

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Card, CardSet, UserProfile, Challenge, Question, Answer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

# Create your views here.


def index(request):
    return HttpResponse("index page test")


def home(request):
    return render(request, "cardgame/home.html")


def card_col(request, user_name):
    """
    Displays a user's card collection.

    Author: BLANK

    Args:
        request: HTTP request object
        user_name: Username whose collection to display

    Returns:
        Rendered template with user's card images or failure message
    """

    # gets the cards from a user's collection and inserts them into the
    # template as context
    try:
        imgs = []
        u = UserProfile.objects.get(user__username=user_name)
        for i in u.user_profile_collected_cards.all():
            print(i.card_image_link)

            # remember, this is an in image field!
            imgs.append(i.card_image_link)
        return render(request, "cardgame/card_col.html", {"images": imgs})

    except ObjectDoesNotExist:
        # if user does not exist
        pass
    return HttpResponse("fail")  # change this later!


def login(LoginView):
    """
    Presumably login
    """
    pass


def signup(request):
    """
    Processes new user registration.

    Author: BLANK

    Args:
        request: HTTP request object containing form data

    Returns:
        HttpResponse: Success/failure message or signup form
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():  # validation later
            try:
                User.objects.create_user(
                    form.cleaned_data["username"], None,
                    form.cleaned_data["password1"]
                )
                return HttpResponse("you did good!")
            except IntegrityError:
                pass
        return HttpResponse("you done goofed!")

    else:
        form = UserCreationForm()
        return HttpResponse(render(request, "cardgame/signup.html",
                                   {"form": form}))


@staff_member_required  # Makes sure only system admins can execute this code
def create_card(request):
    """
    Creates new cards with provided details and images.

    Author: BLANK

    Args:
        request: HTTP request with card data or GET for form

    Returns:
        HttpResponse: Creation status or form template

    Raises:
        400: Missing parameters or invalid card set
    """
    if request.method == "POST":  # Create a card
        # Get info from request
        card_name = request.POST.get("card_name")
        card_subtitle = request.POST.get("card_subtitle")
        card_description = request.POST.get("card_description")
        card_set_name = request.POST.get("card_set")
        card_image = request.FILES.get("card_image")

        # Check that the required parameters are provided
        if not (card_name and card_subtitle and card_description):
            return HttpResponse("Missing required parameters", status=400)

        # Get card set if available
        card_set_instance = None
        if card_set_name:
            try:
                card_set_instance = CardSet.objects.get(
                    card_set_name=card_set_name)
            except CardSet.DoesNotExist:
                return HttpResponse("Specified CardSet does not exist",
                                    status=400)

        try:
            card = Card.objects.create(
                card_name=card_name,
                card_subtitle=card_subtitle,
                card_description=card_description,
                # TODO: add image parameter!!!!
                card_set=card_set_instance,
                card_image_link=card_image,
            )
            return HttpResponse("Card created successfully!")

        # catches errors such as non-unique primary key
        except IntegrityError as e:
            return HttpResponse(f"Error creating card: {e}")
    else:  # GET: Render UI for creating a card
        return render(request, "cardgame/create_card.html")


def get_locations(request):
    """
    Retrieves challenge location data for map display.

    Author: BLANK

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: Formatted location data with coordinates
    """
    locations = list(
        Challenge.objects.select_related("Card").values(
            "Card__card_name", "lat", "long"
        )
    )

    formatted_locations = [
        {
            "name": loc["Card__card_name"],
            "latitude": loc["lat"],
            "longitude": loc["long"],
        }
        for loc in locations
    ]

    return JsonResponse({"locations": formatted_locations})


def signout(request):
    """
    Handles user logout process.

    Author: BLANK

    Args:
        request: HTTP request object

    Returns:
        Redirect to home page
    """
    logout(request)
    redirect("home")  # this is currently bugged!
    # when this is deployed in production, you HAVE to modify the htaccess file
    # so that the ".html" at the end of the URL is removed.
    # proceed with caution! -AGP-


def profile(request, user_name):
    """
    Displays user profile information.

    Author: BLANK

    Args:
        request: HTTP request object
        user_name: Username to display profile for

    Returns:
        HttpResponse: Profile data or failure message
    """
    try:
        u = UserProfile.objects.get(user__username=user_name)
        ctx = {"username": user_name}  # puts out the username at the moment
        # return render(request, "cardgame/profile.html", ctx)
        # profile.html not implemented yet!
        return HttpResponse("profile of " + user_name)

    except ObjectDoesNotExist:
        pass

    return HttpResponse("failure!")  # do something more verbose


def challenge(request, challenge_id):
    """
    Manages challenge interactions and responses.

    Author: BLANK

    Args:
        request: HTTP request object
        challenge_id: ID of the challenge to process

    Returns:
        HttpResponse: Challenge data or failure message
    """
    # we need to get the challenge, the questions, and the answers.
    try:
        pass

    except ObjectDoesNotExist:
        pass

    return HttpResponse("failure!")
