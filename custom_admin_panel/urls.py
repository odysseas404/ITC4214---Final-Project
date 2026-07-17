# Imports the path function so URL routes can be defined.
from django.urls import path

# Imports the views from the custom_admin_panel app.
from . import views


# App namespace used in templates.
app_name = "custom_admin_panel"


urlpatterns = [
    # Custom admin dashboard.
    path("", views.admin_dashboard, name="admin_dashboard"),

    # Borrow request management page.
    path("borrow-requests/", views.manage_borrow_requests, name="manage_borrow_requests"),

    # Updates the status of a borrow request.
    path(
        "borrow-requests/<int:request_id>/status/<str:new_status>/",
        views.update_borrow_status,
        name="update_borrow_status"
    ),

    # Camera management page.
    path("cameras/", views.manage_cameras, name="manage_cameras"),

    # Add camera page.
    path("cameras/add/", views.add_camera, name="add_camera"),

    # Delete camera action.
    path("cameras/<int:camera_id>/delete/", views.delete_camera, name="delete_camera"),
]