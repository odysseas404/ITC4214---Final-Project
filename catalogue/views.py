from django.shortcuts import render, get_object_or_404
from .models import Camera


def camera_detail(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)

    return render(request, "catalogue/camera_detail.html", {
        "camera": camera
    })