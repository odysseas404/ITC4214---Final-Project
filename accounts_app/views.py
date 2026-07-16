# Imports functions used to render templates and redirect users.
from django.shortcuts import render, redirect, get_object_or_404

# Imports Django's login function.
from django.contrib.auth import login

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
    borrow_requests = BorrowRequest.objects.filter(
        user=request.user
    ).select_related("camera").order_by("-created_at")

    liked_cameras = Camera.objects.filter(
        likes__user=request.user
    )

    return render(request, "accounts_app/dashboard.html", {
        "borrow_requests": borrow_requests,
        "liked_cameras": liked_cameras,
    })


# Displays the user's profile page.
@login_required
def profile(request):
    return render(request, "accounts_app/profile.html")


# Allows the user to edit their profile information.
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("accounts_app:profile")

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts_app/edit_profile.html", {
        "form": form
    })


# Allows a logged-in user to cancel one of their own pending borrow requests.
@login_required
def cancel_borrow_request(request, request_id):
    borrow_request = get_object_or_404(
        BorrowRequest,
        id=request_id,
        user=request.user
    )

    if request.method == "POST":
        if borrow_request.status == "Pending":
            borrow_request.delete()

    return redirect("accounts_app:dashboard")