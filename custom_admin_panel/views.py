# Imports functions used to render templates, find objects, and redirect users.
from django.shortcuts import render, get_object_or_404, redirect

# Imports decorators used to protect views.
from django.contrib.auth.decorators import login_required, user_passes_test

# Imports ProtectedError so the camera delete view can handle protected objects.
from django.db.models import ProtectedError

# Imports the models managed by the custom admin panel.
from catalogue.models import Camera, BorrowRequest

# Imports the form used to add new camera listings.
from .forms import CameraForm

# Imports custom permission checks for the custom admin roles.
from .permissions import (
    can_view_custom_admin,
    can_manage_borrowing,
    can_manage_catalogue,
)


# Main custom admin dashboard.
@login_required
@user_passes_test(can_view_custom_admin)
def admin_dashboard(request):
    camera_count = Camera.objects.count()

    pending_requests_count = BorrowRequest.objects.filter(
        status="Pending"
    ).count()

    return render(request, "custom_admin_panel/admin_dashboard.html", {
        "camera_count": camera_count,
        "pending_requests_count": pending_requests_count,
    })


# Page for managing borrow requests.
@login_required
@user_passes_test(can_manage_borrowing)
def manage_borrow_requests(request):
    borrow_requests = BorrowRequest.objects.select_related(
        "user",
        "camera"
    ).order_by("-created_at")

    return render(request, "custom_admin_panel/manage_borrow_requests.html", {
        "borrow_requests": borrow_requests,
    })


# Allows a borrowing manager or administrator to update request status.
@login_required
@user_passes_test(can_manage_borrowing)
def update_borrow_status(request, request_id, new_status):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    allowed_statuses = [
        "Pending",
        "Approved",
        "Borrowed",
        "Returned",
        "Completed",
        "Rejected",
    ]

    if new_status in allowed_statuses:
        borrow_request.status = new_status
        borrow_request.save()

    return redirect("custom_admin_panel:manage_borrow_requests")


# Page for managing camera listings.
@login_required
@user_passes_test(can_manage_catalogue)
def manage_cameras(request):
    cameras = Camera.objects.select_related(
        "manufacturer",
        "category"
    ).order_by("name")

    return render(request, "custom_admin_panel/manage_cameras.html", {
        "cameras": cameras
    })


# Allows a catalogue manager or administrator to add a new camera listing.
@login_required
@user_passes_test(can_manage_catalogue)
def add_camera(request):
    if request.method == "POST":
        form = CameraForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("custom_admin_panel:manage_cameras")

    else:
        form = CameraForm()

    return render(request, "custom_admin_panel/add_camera.html", {
        "form": form
    })


# Allows a catalogue manager or administrator to remove a camera listing.
@login_required
@user_passes_test(can_manage_catalogue)
def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)

    if request.method == "POST":
        try:
            camera.delete()

        # If the camera has borrow request history, it cannot be deleted.
        # In that case, the camera is marked as unavailable instead.
        except ProtectedError:
            camera.available = False
            camera.save()

    return redirect("custom_admin_panel:manage_cameras")