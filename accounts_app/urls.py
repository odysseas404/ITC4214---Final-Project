# Imports the path function so URL routes can be defined.
from django.urls import path

# Imports the views from the accounts_app.
from . import views


# App namespace used in templates, for example accounts_app:dashboard.
app_name = "accounts_app"


urlpatterns = [
    # Registration page.
    path("register/", views.register, name="register"),

    # User dashboard page.
    path("dashboard/", views.dashboard, name="dashboard"),

    # User profile page.
    path("profile/", views.profile, name="profile"),

    # Edit profile page.
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Cancels a pending borrow request that belongs to the logged-in user.
    path(
        "borrow-request/<int:request_id>/cancel/",
        views.cancel_borrow_request,
        name="cancel_borrow_request"
    ),
]