from django.urls import path
from . import views

app_name = "borrowing"

urlpatterns = [
    path("basket/", views.borrow_basket, name="borrow_basket"),
    path("basket/add/<int:camera_id>/", views.add_to_borrow_basket, name="add_to_borrow_basket"),
    path("basket/remove/<int:camera_id>/", views.remove_from_borrow_basket, name="remove_from_borrow_basket"),
    path("basket/checkout/", views.borrow_checkout, name="borrow_checkout"),
    path("success/", views.borrow_success, name="borrow_success"),
]