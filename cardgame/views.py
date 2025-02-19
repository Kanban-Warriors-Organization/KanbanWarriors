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
from .models import Card, CardSet, UserProfile, Challenge, Question
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.templatetags.static import static
import datetime

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
        Rendered template with user's card images or failure message. Seperates cards into either being owned or not
        owned by the user and sends each cards information to the template.
    """
    try:
        imgs_has = []
        imgs_not = []
        card_titleshas = []
        card_descriptionshas = []
        u = UserProfile.objects.get(user__username=user_name)
        for i in u.user_profile_collected_cards.all():
            imgs_has.append(i.card_image_link)
            card_titleshas.append(i.card_name)
            card_descriptionshas.append(i.card_description)
        for j in Card.objects.all():
            imgs_not.append(j.card_image_link)
        imgs_not = list(filter(lambda x: x not in imgs_has, imgs_not))

        cards_has = [{"image": img, "title": title, "description": description}
                     for img, title, description in zip(imgs_has, card_titleshas, card_descriptionshas)]
        return render(request, "cardgame/card_col.html", {"cardshas": cards_has, "imgsnot": imgs_not})

    except ObjectDoesNotExist:
        # if user does not exist
        pass
    return HttpResponse("fail")  # change this later!

def recent_card_data(request):
    """
    Finds the most recently created card and returns its
    """
    recent_card = Card.objects.order_by('-card_created_at').first()
    data = {
            "name": recent_card.card_name,
            "description": recent_card.card_description,
            "image": recent_card.card_image_link.url
        }

    return JsonResponse(data)

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
        Challenge.objects.select_related("card").values(
            "card__card_name", "latitude", "longitude"
        )
    )

    formatted_locations = [
        {
            "name": loc["card__card_name"],
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
        }
        for loc in locations
    ]

    return JsonResponse({"locations": formatted_locations})

def leaderboard_data(request):
    top_players = UserProfile.objects.order_by('-user_profile_points')[:5] # Retrives Top 5 Players
    data = [
        {"username": player.user.username, "points": player.user_profile_points}
        for player in top_players
    ]
    return JsonResponse(data, safe=False)

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


def challenges(request):

    """Renders the "all challenges" page
    Author: adam
    Args: request: HTTP request object
    Returns: renders the template "challenges.html" with the details of all active challenges as context
    """


    try:
        ctime = datetime.now()
        challenges = Challenge.objects.filter(start_time__lte=ctime, end_time__gte=ctime) #filters all challenges that are ongoing
        chals = []
        for c in challenges:
            d = {'long':c.long, 'lat':c.lat, 'start':c.start, 'end':c.end,
                 'card_name':c.card.name, 'points':c.points_reward,
                 'desc':c.description, 'image_link':c.card.card_image_link} #dict with all relevant properties
            chals.append(c)

        return render(request, "challenges.html", {'challenges':chals}) #renders the template


    except ObjectDoesNotExist:
        return HttpResponse("something went really wrong here!")



def challenge(request, chal_id):
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

    if request.method == 'POST':
        pass #redirect and stuff

    else:
        try:
            c = Challenge.objects.get(id = chal_id)
            #pass context into the template
            c.update_status()
            valid = True if c.status == 'ongoing' else False


        except ObjectDoesNotExist:
            pass


    return HttpResponse("failure!")
