from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from catalogue.models import BorrowRequest, Camera
from .forms import TravellerRegistrationForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = TravellerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts_app:dashboard")

    else:
        form = TravellerRegistrationForm()

    return render(request, "accounts_app/register.html", {
        "form": form
    })


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


@login_required
def profile(request):
    return render(request, "accounts_app/profile.html")


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