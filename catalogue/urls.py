#Imports the path function so we can define URL routes.
from django.urls import path

#Imports the views.py file from the same app.
from . import views

#App namespace, which allows us to refer to catalogue URLS as catalogue:home, catalogue:camera_detail, catalogue:about.
app_name = "catalogue"

#URL patterns for the catalogue app; Each path connects a URL to a view function and gives it a nickname using name="".
urlpatterns = [
    path("", views.home, name="home"),
    #Detail page for one specific camera. The <int:camera_id> part captures the camera's id from the URL.
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),
    path("about/", views.about, name="about"),
]