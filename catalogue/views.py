from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Camera, Category, Manufacturer, BorrowRequest, CameraLike 
from .forms import BorrowRequestForm, UserUpdateForm

def home(request):
    cameras = Camera.objects.select_related(
        "category",
        "manufacturer"
    ).filter(available=True)

    search_query = request.GET.get("search")
    manufacturer_id = request.GET.get("manufacturer")
    film_format = request.GET.get("film_format")
    condition = request.GET.get("condition")
    trip_type = request.GET.get("trip_type")

    if search_query:
        cameras = cameras.filter(name__icontains=search_query)

    if manufacturer_id:
        cameras = cameras.filter(manufacturer_id=manufacturer_id)

    if film_format:
        cameras = cameras.filter(film_format=film_format)

    if condition:
        cameras = cameras.filter(condition=condition)

    if trip_type:
        cameras = cameras.filter(recommended_trip_type=trip_type)

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return render(request, "catalogue/home.html", {
        "cameras": cameras,
        "categories": categories,
        "manufacturers": manufacturers,
        "film_format_choices": Camera.FILM_FORMAT_CHOICES,
        "condition_choices": Camera.CONDITION_CHOICES,
        "trip_type_choices": Camera.TRIP_TYPE_CHOICES,
    })


def camera_detail(request, camera_id):
    camera = get_object_or_404(
        Camera.objects.select_related(
            "category",
            "manufacturer"
        ).prefetch_related("gallery_images"),
        id=camera_id
    )

    user_liked = False

    if request.user.is_authenticated:
        user_liked = CameraLike.objects.filter(
            user=request.user,
            camera=camera
        ).exists()

    recommended_cameras = Camera.objects.filter(
        available=True
    ).exclude(
        id=camera.id
    ).filter(
        film_format=camera.film_format
    )[:3]

    if not recommended_cameras:
        recommended_cameras = Camera.objects.filter(
        available=True
    ).exclude(
        id=camera.id
    ).filter(
        recommended_trip_type=camera.recommended_trip_type
    )[:3]

    return render(request, "catalogue/camera_detail.html", {
        "camera": camera,
        "user_liked": user_liked,
        "recommended_cameras": recommended_cameras,
    })

@login_required
def borrow_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id, available=True)

    if request.method == "POST":
        form = BorrowRequestForm(request.POST)

        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.user = request.user
            borrow_request.camera = camera
            borrow_request.save()

            return redirect("catalogue:borrow_success")

    else:
        form = BorrowRequestForm()

    return render(request, "catalogue/borrow_camera.html", {
        "form": form,
        "camera": camera,
    })


@login_required
def borrow_success(request):
    return render(request, "catalogue/borrow_success.html")


@login_required
def dashboard(request):
    borrow_requests = BorrowRequest.objects.filter(
        user=request.user
    ).select_related("camera").order_by("-created_at")

    return render(request, "catalogue/dashboard.html", {
        "borrow_requests": borrow_requests,
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("catalogue:dashboard")

    else:
        form = UserCreationForm()

    return render(request, "catalogue/register.html", {
        "form": form
    })

@login_required
def profile(request):
    return render(request, "catalogue/profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("catalogue:profile")

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "catalogue/edit_profile.html", {
        "form": form
    })

@login_required
def toggle_like(request, camera_id):
    if request.method == "POST":
        camera = get_object_or_404(Camera, id=camera_id)

        like, created = CameraLike.objects.get_or_create(
            user=request.user,
            camera=camera
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False

        like_count = camera.likes.count()

        return JsonResponse({
            "liked": liked,
            "like_count": like_count
        })

    return JsonResponse({
        "error": "Invalid request"
    }, status=400)

@login_required
def add_to_borrow_basket(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id, available=True)

    basket = request.session.get("borrow_basket", [])

    if camera.id not in basket:
        basket.append(camera.id)

    request.session["borrow_basket"] = basket

    return redirect("catalogue:borrow_basket")

@login_required
def borrow_basket(request):
    basket = request.session.get("borrow_basket", [])

    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    ).select_related("manufacturer", "category")

    return render(request, "catalogue/borrow_basket.html", {
        "cameras": cameras
    })

@login_required
def remove_from_borrow_basket(request, camera_id):
    basket = request.session.get("borrow_basket", [])

    if camera_id in basket:
        basket.remove(camera_id)

    request.session["borrow_basket"] = basket

    return redirect("catalogue:borrow_basket")

@login_required
def borrow_checkout(request):
    basket = request.session.get("borrow_basket", [])

    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    )

    if not cameras:
        return redirect("catalogue:borrow_basket")

    if request.method == "POST":
        form = BorrowRequestForm(request.POST)

        if form.is_valid():
            for camera in cameras:
                borrow_request = form.save(commit=False)
                borrow_request.user = request.user
                borrow_request.camera = camera
                borrow_request.pk = None
                borrow_request.save()

            request.session["borrow_basket"] = []

            return redirect("catalogue:borrow_success")

    else:
        form = BorrowRequestForm()

    return render(request, "catalogue/borrow_checkout.html", {
        "form": form,
        "cameras": cameras
    })