from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from catalogue.models import Camera
from .forms import BorrowRequestForm

#Adds a selected camera to the user's Borrow Basket.
@login_required
def add_to_borrow_basket(request, camera_id):

    #Get the selected camera only if it is currently available.
    camera = get_object_or_404(Camera, id=camera_id, available=True)

    #Get the current basket from the session - if it doesn't exist, create an empty list.
    basket = request.session.get("borrow_basket", [])

    #Add the camera id only if it is not already in the basket.
    if camera.id not in basket:
        basket.append(camera.id)

    #Save the updated basket back into the session.
    request.session["borrow_basket"] = basket

    #Redirect the user to the Borrow Basket page.
    return redirect("borrowing:borrow_basket")

#Display's the user's current Borrow Basket.
@login_required
def borrow_basket(request):

    #Get the basket from the session.
    basket = request.session.get("borrow_basket", [])

    #Get all available cameras whose ids are stored in the basket - select_related reduces database queries for manufacturer and category.
    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    ).select_related("manufacturer", "category")

    #Render the Borrow Basket template.
    return render(request, "borrowing/borrow_basket.html", {
        "cameras": cameras
    })

#Removes a selected camera from the user's Borrow Basket.
@login_required
def remove_from_borrow_basket(request, camera_id):
    basket = request.session.get("borrow_basket", [])

    if camera_id in basket:
        basket.remove(camera_id)

    request.session["borrow_basket"] = basket

    return redirect("borrowing:borrow_basket")

#Displays and processes the checkout form for borrow requests.
@login_required
def borrow_checkout(request):
    basket = request.session.get("borrow_basket", [])

    cameras = Camera.objects.filter(
        id__in=basket,
        available=True
    )

    #If the basket is empty, send the user back to the Borrow Basket page.
    if not cameras:
        return redirect("borrowing:borrow_basket")

    #If the user submitted the form, process the submitted data.
    if request.method == "POST":
        form = BorrowRequestForm(request.POST)

        #If the form passes validation, create borrow requests.
        if form.is_valid():

            #Create one borrow request for each camera in the basket.
            for camera in cameras:
                borrow_request = form.save(commit=False)

                #Connect the request to the logged-in user.
                borrow_request.user = request.user
                borrow_request.camera = camera

                #Make sure Django creates a new object for each camera.
                borrow_request.pk = None

                #Save the borrow request to the database.
                borrow_request.save()

            #Empty the basket after the requests have been submitted.
            request.session["borrow_basket"] = []

            return redirect("borrowing:borrow_success")

    else:
        form = BorrowRequestForm()

    return render(request, "borrowing/borrow_checkout.html", {
        "form": form,
        "cameras": cameras
    })

#Displays the success page after a borrow request is submitted.
@login_required
def borrow_success(request):
    return render(request, "borrowing/borrow_success.html")