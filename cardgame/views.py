"""
Core functionality for user interactions, authentication, and data management.
Handles routing and processing for user profiles, card collections, challenges,
and administrative functions.
"""

import random
import sys
import datetime
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

# from django.template import loader
from django.contrib.auth import logout, login  # authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from image_gen import make_image
from .models import Card, CardSet, UserProfile, Challenge, Question
import uuid


def index(request):
    """
    Default index landing page
    """
    form = UserCreationForm()
    return HttpResponse(render(request, "cardgame/signup.html", {"form": form}))


def home(request):
    """
    Renders the homepage.
    """
    return render(request, "cardgame/home.html")


def collection_redirect(request):
    return redirect(
        reverse("cardcollection", kwargs={"user_name": request.user.username})
    )


def card_col(request, user_name):
    """
    Displays a user's card collection.

    Author: BLANK

    Args:
        request: HTTP request object
        user_name: Username whose collection to display

    Returns:
        Rendered template with user's card images or failure message.
        Seperates cards into either being owned or not
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

        cards_has = [
            {"image": img, "title": title, "description": description}
            for img, title, description in zip(
                imgs_has, card_titleshas, card_descriptionshas
            )
        ]
        return render(
            request,
            "cardgame/card_col.html",
            {"cardshas": cards_has, "imgsnot": imgs_not},
        )

    except ObjectDoesNotExist:
        # if user does not exist
        raise Http404()
    return HttpResponse("fail")  # change this later!


def recent_card_data(request):
    """
    Finds the most recently created card and returns its
    """
    recent_card = Card.objects.order_by("-card_created_at").first()
    data = {
        "name": recent_card.card_name,
        "description": recent_card.card_description,
        "image": recent_card.card_image_link.url,
    }

    return JsonResponse(data)


def signup(request):
    """
    Processes new user registration.

    Author: Adam

    Args:
        request: HTTP request object containing form data

    Returns:
        HttpResponse: Success/failure message or signup form
    """

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # Validates the contents of the form.
        # Since we're using a DJANGO inbuilt form, this is
        # handled automatically.
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                # Creates user and user profile objects
                user = User.objects.create_user(
                    username, None, form.cleaned_data["password1"]
                )
                new_user_profile = UserProfile.create(user)
                new_user_profile.save()
                login(request, user)
                messages.success(request, "Account Created!")
                return redirect(f"/user/{username}/profile")
            except IntegrityError:
                pass
        messages.error(request, "Account with that name already exists!")
        return HttpResponse(render(request, "cardgame/signup.html", {"form": form}))

    # GET request: gets and renders the form.
    else:
        form = UserCreationForm()
        return HttpResponse(render(request, "cardgame/signup.html", {"form": form}))


@staff_member_required  # Makes sure only system admins can execute this code
def create_card(request):
    """
    Creates new cards with provided details and images.

    Author: Sam, Adam (for the parts pertaining to image generation)

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
        card_cost = int(request.POST.get("cost", 0))
        card_beauty = int(request.POST.get("beauty", 0))
        card_env = int(request.POST.get("environmental_friendliness", 0))
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

            # Generates card image with given script.
            c = make_image(
                "static/card_gen/back.png",
                card_name,
                card_subtitle,
                "static/card_gen/normal.ttf",
                "static/card_gen/bold.ttf",
                card_description,
                card_image,
                card_env,
                card_beauty,
                card_cost,
            )

            c_io = BytesIO()
            c.save(c_io, format="PNG")
            # We have to convert from a PIL image to a DJANGO image
            django_file = InMemoryUploadedFile(
                c_io,
                None,
                str(card_name).replace(" ", "_") + ".png",
                "image/png",
                sys.getsizeof(c_io),
                None,
            )

            # Creates the card object and saves to database
            card = Card.objects.create(
                card_name=card_name,
                card_subtitle=card_subtitle,
                card_description=card_description,
                card_set=card_set_instance,
                card_image_link=django_file,
                environmental_friendliness=card_env,
                beauty=card_beauty,
                cost=card_cost,
            )
            card.save()

            return HttpResponse("Card created successfully!")

        # catches errors such as non-unique primary key
        except IntegrityError as e:
            return HttpResponse(f"Error creating card: {e}")
    else:  # GET: Render UI for creating a card
        return render(request, "cardgame/create_card.html")


def get_locations(request):
    """
    Retrieves challenge location data for map display.

    Author: Jake Klar

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: Formatted location data with coordinates
    """

    upc = UserProfile.objects.get(user=request.user).user_profile_collected_cards.all()
    print(upc)
    challenges = Challenge.objects.exclude(card__in=upc)
    locations = list(
        challenges.select_related("card").values(
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
    """
    Returns the data required for the leaderboard,
    namely the 5 users with the highest score
    and their respective scores.

    Author: Jake Klar

    Args:
        request: HTTP request object

    Returns:
        The required leaderboard data
    """

    top_players = UserProfile.objects.order_by("-user_profile_points")[
        :5
    ]  # Retrieves Top 5 Players
    data = [
        {"username": player.user.username, "points": player.user_profile_points}
        for player in top_players
    ]
    return JsonResponse(data, safe=False)  # Returns JSON response to template


@login_required
def log_out(request):
    """
    Handles user logout process by logging out the user
    and redirecting to the homepage.

    Author: Adam

    Args:
        request: HTTP request object

    Returns:
        Redirect to home page
    """
    logout(request)
    return redirect("login")


def profile_redirect(request):
    """
    Redirects to a user's profile
    """
    return redirect(reverse("profile", kwargs={"user_name": request.user.username}))


def profile(request, user_name):
    """
    Displays user profile information.

    Author: Adam

    Args:
        request: HTTP request object
        user_name: Username to display profile for

    Returns:
        HttpResponse: Profile data or failure message
    """
    try:
        u = UserProfile.objects.get(user__username=user_name)
        # get number of cards in total
        card_num = Card.objects.all().count()
        user_card_num = u.user_profile_collected_cards.all().count()
        card_id = u.user_most_recent_card

        # failsafe for if the user has no cards
        if card_id == "nocards":
            recent_card_name = None
            recent_card_image = None
            recent_card_date = None

        # if there is cards, gets the relevant data
        else:
            rec_card = Card.objects.get(card_name=card_id)
            recent_card_name = rec_card.card_name
            recent_card_image = rec_card.card_image_link
            recent_card_date = u.user_most_recent_card_date

        ctx = {
            "username": user_name,
            "card_num": card_num,
            "user_card_num": user_card_num,
            "recent_card_date": recent_card_date,
            "user_reg_date": u.user_signup_date,
            "recent_card_name": recent_card_name,
            "recent_card_image": recent_card_image,
            "points": u.user_profile_points,
        }

        # renders profile template with context
        return render(request, "cardgame/profile.html", ctx)

    except ObjectDoesNotExist:
        raise Http404()


@login_required
def challenges(request):
    """Renders the "all challenges" page
    Author: adam
    Args: request: HTTP request object
    Returns: renders the template "challenges.html" with the
    details of all active challenges as context
    """

    try:
        ctime = datetime.datetime.now()
        upc = UserProfile.objects.get(user=request.user).user_profile_collected_cards
        # filters all challenges that are ongoing
        challenges = Challenge.objects.filter(
            start_time__lte=ctime, end_time__gte=ctime
        )
        chals = []
        available = False
        # checks if there are challenges available, needed to prevent fails
        if challenges.count != 0:
            available: bool = True
            for c in challenges:
                # verifies that the user doesn't already
                # have the associated card
                if c.card not in upc.all():
                    d = {
                        "longitude": c.longitude,
                        "latitude": c.latitude,
                        "start": c.start_time,
                        "end": c.end_time,
                        "card_name": c.card.card_name,
                        "points": c.points_reward,
                        "desc": c.description,
                        "image_link": c.card.card_image_link,
                        "id": c.id,
                    }  # dict with all relevant properties
                    chals.append(d)

        # renders the template
        return render(
            request,
            "cardgame/challenges.html",
            {"challenges": chals, "open_chals": available},
        )

    except ObjectDoesNotExist:
        raise Http404()


@login_required
def challenge(request, chal_id):
    """
    Manages challenge interactions and responses.

    Author: Adam

    Args:
        request: HTTP request object
        chal_id: ID of the challenge to process

    Returns:
        HttpResponse: Challenge data or failure message
    """
    # we need to get the challenge, the questions, and the answers.
    if request.method == "GET":  # for rendering the page initially
        try:
            # checks that the user doesn't already have the card
            user = request.user
            up = UserProfile.objects.get(user=user)
            chal = Challenge.objects.get(id=chal_id)
            if chal.card in up.user_profile_collected_cards.all():
                return HttpResponse("sorry, you already have this card!")

            # gets challenge information
            info = {
                "longitude": chal.longitude,
                "latitude": chal.latitude,
                "start": chal.start_time,
                "end": chal.end_time,
                "card_name": chal.card.card_name,
                "points": chal.points_reward,
                "desc": chal.description,
                "image_link": chal.card.card_image_link,
                "id": chal.id,
            }

            # gets challenge questions
            questions = []
            quest_set = Question.objects.filter(challenge__id=chal_id)
            for question in quest_set:
                q_details = {
                    "question": question.text,
                    "ans1": question.option_a,
                    "ans2": question.option_b,
                    "ans3": question.option_c,
                    "ans4": question.option_d,
                    "right_ans": question.correct_answer,
                }
                questions.append(q_details)

            # renders challenge template with context
            return render(
                request,
                "cardgame/verification.html",
                {"info": info, "questions": questions},
            )
        # raises a 404 if the user tries to access a
        # challenge that does not exist
        except ObjectDoesNotExist:
            raise Http404()
        return HttpResponse("failure!")


def add_card(request, chal_id):
    """
    Adds a card to a user's profile upon completion of a challenge
    Written by Adam

    Args:
        request: a HTTP request object
        chal_id: the identifier of the challenge that has been completed

    Returns:
        a HTTP response object
    """
    # Gets the card from the challenge.
    c = Challenge.objects.get(id=chal_id)
    card = c.card
    # gets the user
    u = request.user
    # gets the user profile
    up = UserProfile.objects.get(user=u)
    # gives the user the card
    if not (up.user_profile_collected_cards.filter(card_name=card.card_name).exists()):

        up.user_profile_collected_cards.add(card)
        # Gives the user the points for the card
        up.user_profile_points = up.user_profile_points + c.points_reward
        up.user_most_recent_card = card.card_name
        up.user_most_recent_card_date = datetime.datetime.now()

        up.save()

    return HttpResponse(request)


def echo_user(request):
    u = request.user
    return HttpResponse(str(u))


@login_required
def battle_room(request, room_id=None):
    """
    Renders the battle room page where users can battle with their cards.

    Author: Samuel

    Args:
        request: HTTP request object
        room_id: Optional room ID parameter

    Returns:
        Rendered battle room template
    """
    if room_id is None:
        # Generate a new room ID if none is provided
        room_id = str(uuid.uuid4())[:8]
        return redirect("battle_with_id", room_id=room_id)

    return render(
        request,
        "cardgame/battle.html",
        {"room_id": room_id, "username": request.user.username},
    )


@login_required
def get_battle_cards(request):
    """
    Retrieves cards available for battle from user's collection.

    Author: Samuel

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: User's collected cards with battle stats
    """
    try:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        cards = user_profile.user_profile_collected_cards.all()

        card_data = []
        for card in cards:
            card_data.append(
                {
                    "name": card.card_name,
                    "subtitle": card.card_subtitle,
                    "description": card.card_description,
                    "image": card.card_image_link.url if card.card_image_link else None,
                    "environmental_friendliness": (
                        card.environmental_friendliness
                        if hasattr(card, "environmental_friendliness")
                        else random.randint(1, 10)
                    ),
                    "beauty": (
                        card.beauty
                        if hasattr(card, "beauty")
                        else random.randint(1, 10)
                    ),
                    "cost": (
                        card.cost if hasattr(card, "cost") else random.randint(1, 10)
                    ),
                }
            )

        return JsonResponse({"cards": card_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def battle_select(request):
    """
    Renders the battle selection screen where users can create or join battles.

    Author: Samuel
    """
    return render(request, "cardgame/battle_select.html")
