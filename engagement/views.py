from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from catalogue.models import Camera, CameraLike


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