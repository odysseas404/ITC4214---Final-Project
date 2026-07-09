from django.urls import path
from . import views

app_name = "custom_admin_panel"

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("borrow-requests/", views.manage_borrow_requests, name="manage_borrow_requests"),
    path("borrow-requests/<int:request_id>/status/<str:new_status>/", views.update_borrow_status, name="update_borrow_status"),
    path("cameras/", views.manage_cameras, name="manage_cameras"),
]