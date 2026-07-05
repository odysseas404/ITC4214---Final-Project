from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.home, name="home"),
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),
    path("camera/<int:camera_id>/borrow/", views.borrow_camera, name="borrow_camera"),
    path("borrow/success/", views.borrow_success, name="borrow_success"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
]