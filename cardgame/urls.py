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
    path("profile-redirect/", views.profile_redirect, name="profile-redirect"),
    path("collection-redirect/", views.collection_redirect,
         name="collection-redirect"),
    path("challenges/", views.challenges, name="challenges"),  # [1]
    path("echo_user", views.echo_user, name="echo_user"),
    path("trades/", views.global_trade_page, name="search"),
    path("trades/search/", views.get_trades_matching_query,
         name="search_results"),
    path("trades/personal", views.get_personal_trades, name="personal"),
    path("trades/create/<str:card_name>/", views.make_trade_page, name="create"),
    path("trades/submit", views.submit_trade, name="submit"),
    path("trade/<int:t_id>/accept", views.accept_trade, name="accept"),
    path("trade/<int:t_id>/cancel", views.cancel_trade, name="cancel"),
    path("privacy/", views.privacy, name="privacy"),
    path("account", views.account, name="account"),
    path("change_username", views.change_username, name="change_username"),
    path("change_password",
         auth_views.PasswordChangeView
         .as_view(template_name="cardgame/change_password.html",
                  success_url="home"),
         name="change_password"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("reset_password", auth_views.PasswordResetView
         .as_view(template_name="cardgame/reset.html"),
         name="reset_password"),

    # uses django's inbuilt login view
    path('battle/', views.battle_room, name='battle'),
    path('battle/<str:room_id>/', views.battle_room, name='battle_with_id'),
    path("get-battle-cards/", views.get_battle_cards, name="get_battle_cards"),
    path('battle-select/', views.battle_select, name='battle_select'),
]   # [1] DO NOT REMOVE THE SLASH!

# (template_name="cardgame/login.html")
