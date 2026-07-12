from django.shortcuts import get_object_or_404

#Makes sure only logged-in users can like or unlike cameras.
from django.contrib.auth.decorators import login_required

#Allows the view to return data in JSON format form JavaScript.
from django.http import JsonResponse

#Imports the Camera and CameraLike models from the catalogue app.
from catalogue.models import Camera, CameraLike

#The user must be logged in to use this view, which handles liking and unliking a camera.
@login_required
def toggle_like(request, camera_id):

    #Only allow POST requests for this action.
    if request.method == "POST":
        camera = get_object_or_404(Camera, id=camera_id)

        #Get an existing like or create a new one. 
        like, created = CameraLike.objects.get_or_create(
            user=request.user,
            camera=camera
        )

        #If a new like was created, the camera is now liked.
        if created:
            liked = True

        #If the like already existed, delete it to unlike the camera.
        else:
            like.delete()
            liked = False

        like_count = camera.likes.count()

        #Return the result to JavaScript.
        return JsonResponse({
            "liked": liked,
            "like_count": like_count
        })
    
    #If the request is not POST, return an error request.
    return JsonResponse({
        "error": "Invalid request"
    }, status=400)