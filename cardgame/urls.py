"""
URL configuration.

This module defines the URL patterns.

Author: BLANK
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("locations-data/", views.get_locations, name="locations_data"),
    path("user/<str:user_name>/cards", views.card_col, name="cardcollection"),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="cardgame/login.html"),
        name="login",
    ),
    path("signup", views.signup, name="signup"),
    path("create_card", views.create_card, name="create_card"),
    path("logout", views.log_out, name="logout"),
    path("leaderboard-data/", views.leaderboard_data, name="leaderboard_data"),
    path("recent-card-data/", views.recent_card_data, name="recent_card_data"),
    path("user/<str:user_name>/profile", views.profile, name="profile"),
    path("challenge/<int:chal_id>", views.challenge, name="challenge"),
    path("add-card/<int:chal_id>", views.add_card, name="add-card"),
    path("challenges/", views.challenges, name="challenges"), #DO NOT REMOVE THE SLASH!
    path("echo_user", views.echo_user, name="echo_user")
    # uses django's inbuilt login view
]

# (template_name="cardgame/login.html")
