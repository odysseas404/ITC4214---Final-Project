from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.home, name="home"),
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("about/", views.about, name="about"),
]