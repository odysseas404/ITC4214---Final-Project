from django.urls import path
from . import views

app_name = "engagement"

urlpatterns = [
    path("camera/<int:camera_id>/like/", views.toggle_like, name="toggle_like"),
]