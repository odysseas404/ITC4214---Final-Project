from django.urls import path
from . import views

#App namespace, allowing us to refer to this app's URLs as engagement:toggle_like.
app_name = "engagement"

urlpatterns = [
  
    #URL used when a logged-in user likes or unlikes the camera. The <int:camera_id> part captures the camera id from the URL.
    path("camera/<int:camera_id>/like/", views.toggle_like, name="toggle_like"),
]