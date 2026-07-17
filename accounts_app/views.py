# Imports functions used to render templates, redirect users, and get objects.
from django.shortcuts import render, redirect, get_object_or_404

# Imports Django's login function and keeps users logged in after password change.
from django.contrib.auth import login, update_session_auth_hash

# Makes sure some views are only available to logged-in users.
from django.contrib.auth.decorators import login_required

# Imports the BorrowRequest and Camera models.
from catalogue.models import BorrowRequest, Camera

# Imports the forms used by the accounts app.
from .forms import TravellerRegistrationForm, UserUpdateForm


# Handles user registration.
def register(request):

    # If the user submitted the registration form, process the submitted data.
    if request.method == "POST":
        form = TravellerRegistrationForm(request.POST)

        # If the form is valid, create the user account.
        if form.is_valid():
            user = form.save()

            # Log in the new user automatically after registration.
            login(request, user)

            # After registration, redirect the user to the homepage.
            return redirect("catalogue:home")

    # If the request is GET, display an empty registration form.
    else:
        form = TravellerRegistrationForm()

    # Render the registration page.
    return render(request, "accounts_app/register.html", {
        "form": form
    })


# Displays the user's dashboard.
@login_required
def dashboard(request):

    # Get all borrow requests submitted by the logged-in user.
    borrow_requests = BorrowRequest.objects.filter(
        user=request.user
    ).select_related("camera").order_by("-created_at")

    # Get all cameras liked by the logged-in user.
    liked_cameras = Camera.objects.filter(
        likes__user=request.user
    ).select_related("manufacturer", "category")

    # Render the dashboard page.
    return render(request, "accounts_app/dashboard.html", {
        "borrow_requests": borrow_requests,
        "liked_cameras": liked_cameras,
    })


# Displays the user's profile page.
@login_required
def profile(request):
    return render(request, "accounts_app/profile.html")


# Allows the user to edit their username, personal details, email, and password.
@login_required
def edit_profile(request):

    # If the user submitted the edit profile form, process the submitted data.
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)

        # If the form is valid, update the user account.
        if form.is_valid():
            user = form.save(commit=False)

            # Get the optional new password from the form.
            new_password = form.cleaned_data.get("new_password")

            # If the user entered a new password, save it securely.
            if new_password:
                user.set_password(new_password)

            # Save the updated user object.
            user.save()

            # Keep the user logged in after changing their password.
            if new_password:
                update_session_auth_hash(request, user)

            # Redirect back to the profile page.
            return redirect("accounts_app:profile")

    # If the request is GET, display the form with the current user information.
    else:
        form = UserUpdateForm(instance=request.user)

    # Render the edit profile page.
    return render(request, "accounts_app/edit_profile.html", {
        "form": form
    })


# Allows a logged-in user to cancel one of their own pending borrow requests.
@login_required
def cancel_borrow_request(request, request_id):

    # Get only a borrow request that belongs to the logged-in user.
    borrow_request = get_object_or_404(
        BorrowRequest,
        id=request_id,
        user=request.user
    )

    # Only allow cancellation through a POST request.
    if request.method == "POST":

        # Only pending requests can be cancelled by the user.
        if borrow_request.status == "Pending":
            borrow_request.delete()

    # Redirect back to the dashboard.
    return redirect("accounts_app:dashboard")