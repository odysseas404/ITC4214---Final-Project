from django.shortcuts import render, get_object_or_404
from .models import Camera, Category, Manufacturer


def home(request):
    cameras = Camera.objects.select_related(
        "category",
        "manufacturer"
    ).filter(available=True)

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return render(request, "catalogue/home.html", {
        "cameras": cameras,
        "categories": categories,
        "manufacturers": manufacturers,
    })


def camera_detail(request, camera_id):
    camera = get_object_or_404(
        Camera.objects.select_related(
            "category",
            "manufacturer"
        ).prefetch_related("gallery_images"),
        id=camera_id
    )

    return render(request, "catalogue/camera_detail.html", {
        "camera": camera
    })