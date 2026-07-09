from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from catalogue.models import Camera
from .forms import BorrowRequestForm


@login_required
def add_to_borrow_basket(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id, available=True)

    basket = request.session.get("borrow_basket", [])

    if camera.id not in basket:
        basket.append(camera.id)

    request.session["borrow_basket"] = basket

    return redirect("borrowing:borrow_basket")


@login_required
def borrow_basket(request):
    basket = request.session.get("borrow_basket", [])

    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    ).select_related("manufacturer", "category")

    return render(request, "borrowing/borrow_basket.html", {
        "cameras": cameras
    })


@login_required
def remove_from_borrow_basket(request, camera_id):
    basket = request.session.get("borrow_basket", [])

    if camera_id in basket:
        basket.remove(camera_id)

    request.session["borrow_basket"] = basket

    return redirect("borrowing:borrow_basket")


@login_required
def borrow_checkout(request):
    basket = request.session.get("borrow_basket", [])

    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    )

    if not cameras:
        return redirect("borrowing:borrow_basket")

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

            return redirect("borrowing:borrow_success")

    else:
        form = BorrowRequestForm()

    return render(request, "borrowing/borrow_checkout.html", {
        "form": form,
        "cameras": cameras
    })


@login_required
def borrow_success(request):
    return render(request, "borrowing/borrow_success.html")