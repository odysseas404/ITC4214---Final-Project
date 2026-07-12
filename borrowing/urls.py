from django.urls import path
from . import views

#App namespace, which allows us to refer to borrowing URLs as borrowing:borrow_basket etc.
app_name = "borrowing"

urlpatterns = [
    #Shows the user's current Borrow Basket.
    path("basket/", views.borrow_basket, name="borrow_basket"),

    #Adds a selected camera to the Borrow Basket.
    path("basket/add/<int:camera_id>/", views.add_to_borrow_basket, name="add_to_borrow_basket"),

    #Removes a selected camera from the Borrow Basket.
    path("basket/remove/<int:camera_id>/", views.remove_from_borrow_basket, name="remove_from_borrow_basket"),

    #Shows and processes the checkout/borrow request form.
    path("basket/checkout/", views.borrow_checkout, name="borrow_checkout"),

    #Success page shown after a borrow request is submitted.
    path("success/", views.borrow_success, name="borrow_success"),
]