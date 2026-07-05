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
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("camera/<int:camera_id>/toggle_like/", views.toggle_like, name="toggle_like"),
    path("basket/", views.borrow_basket, name="borrow_basket"),
    path("basket/add/<int:camera_id>/", views.add_to_borrow_basket, name="add_to_borrow_basket"),
    path("basket/remove/<int:camera_id>/", views.remove_from_borrow_basket, name="remove_from_borrow_basket"),
    path("basket/checkout/", views.borrow_checkout, name="borrow_checkout"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("about/", views.about, name="about"),
]