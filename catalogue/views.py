from django.shortcuts import render, get_object_or_404

from .models import Camera, Category, Manufacturer, CameraLike


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
    parent_categories = Category.objects.filter(parent__isnull=True)
    manufacturers = Manufacturer.objects.all()

    return render(request, "catalogue/home.html", {
        "cameras": cameras,
        "categories": categories,
        "parent_categories": parent_categories,
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
        available=True,
        film_format=camera.film_format
    ).exclude(
        id=camera.id
    )[:3]

    if not recommended_cameras:
        recommended_cameras = Camera.objects.filter(
            available=True,
            recommended_trip_type=camera.recommended_trip_type
        ).exclude(
            id=camera.id
        )[:3]

    return render(request, "catalogue/camera_detail.html", {
        "camera": camera,
        "user_liked": user_liked,
        "recommended_cameras": recommended_cameras,
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    cameras = Camera.objects.filter(
        category=category,
        available=True
    ).select_related(
        "manufacturer",
        "category"
    )

    return render(request, "catalogue/category_detail.html", {
        "category": category,
        "cameras": cameras,
    })


def about(request):
    return render(request, "catalogue/about.html")