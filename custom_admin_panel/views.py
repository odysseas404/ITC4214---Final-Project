from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from catalogue.models import Camera, BorrowRequest


def is_custom_admin_user(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name="Catalogue Manager").exists()
            or user.groups.filter(name="Borrowing Manager").exists()
        )
    )


def is_catalogue_manager(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name="Catalogue Manager").exists()
        )
    )


def is_borrowing_manager(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name="Borrowing Manager").exists()
        )
    )


@login_required
@user_passes_test(is_custom_admin_user)
def admin_dashboard(request):
    camera_count = Camera.objects.count()
    pending_requests_count = BorrowRequest.objects.filter(status="Pending").count()

    return render(request, "custom_admin_panel/admin_dashboard.html", {
        "camera_count": camera_count,
        "pending_requests_count": pending_requests_count,
    })


@login_required
@user_passes_test(is_borrowing_manager)
def manage_borrow_requests(request):
    borrow_requests = BorrowRequest.objects.select_related(
        "user",
        "camera"
    ).order_by("-created_at")

    return render(request, "custom_admin_panel/manage_borrow_requests.html", {
        "borrow_requests": borrow_requests,
    })


@login_required
@user_passes_test(is_borrowing_manager)
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


@login_required
@user_passes_test(is_catalogue_manager)
def manage_cameras(request):
    cameras = Camera.objects.select_related(
        "manufacturer",
        "category"
    ).order_by("name")

    return render(request, "custom_admin_panel/manage_cameras.html", {
        "cameras": cameras,
    })