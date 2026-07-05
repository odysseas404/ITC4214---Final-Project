from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Camera, Category, Manufacturer, BorrowRequest
from .forms import BorrowRequestForm

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