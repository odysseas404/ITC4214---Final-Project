from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.home, name="home"),
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),
]