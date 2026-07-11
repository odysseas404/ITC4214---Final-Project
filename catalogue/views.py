#Render is used in order to display HTML templates, while the get_object_or_404 is used in order to get one object from the database, or to show a 404 error page if it does not exist.
from django.shortcuts import render, get_object_or_404

# Import the models used by the catalogue views.
from .models import Camera, Manufacturer, CameraLike

def home(request):
    # Get all available cameras from the database; select_related is used for Foreignkey fields, in order to reduce database queries.
    cameras = Camera.objects.select_related(
        "category",
        "manufacturer"
    ).filter(available=True)

    # Get search and filter values from the URL query string.
    search_query = request.GET.get("search")
    manufacturer_id = request.GET.get("manufacturer")
    film_format = request.GET.get("film_format")
    condition = request.GET.get("condition")
    trip_type = request.GET.get("trip_type")

    # Filter cameras by name if the user searched for something.
    if search_query:
        cameras = cameras.filter(name__icontains=search_query)

    # Filter cameras by manufacturer if selected.
    if manufacturer_id:
        cameras = cameras.filter(manufacturer_id=manufacturer_id)

    # Filter cameras by film format if selected.
    if film_format:
        cameras = cameras.filter(film_format=film_format)

    # Filter cameras by condition if selected.
    if condition:
        cameras = cameras.filter(condition=condition)

    # Filter cameras by recommended trip type if selected.
    if trip_type:
        cameras = cameras.filter(recommended_trip_type=trip_type)

    # Get all manufacturers for the manufacturer dropdown filter.
    manufacturers = Manufacturer.objects.all()

    # Send the cameras and filter options to the home template.
    return render(request, "catalogue/home.html", {
        "cameras": cameras,
        "manufacturers": manufacturers,
        "film_format_choices": Camera.FILM_FORMAT_CHOICES,
        "condition_choices": Camera.CONDITION_CHOICES,
        "trip_type_choices": Camera.TRIP_TYPE_CHOICES,
    })

def camera_detail(request, camera_id):
    # Get one camera using its id.
    camera = get_object_or_404(
        Camera.objects.select_related(
            "category",
            "manufacturer"
        ).prefetch_related("gallery_images"),
        id=camera_id
    )

    # By default, assume the user has not liked the camera.
    user_liked = False

    # If the user is logged in, check if they have already liked this camera.
    if request.user.is_authenticated:
        user_liked = CameraLike.objects.filter(
            user=request.user,
            camera=camera
        ).exists()

    # Recommend cameras with the same film format.
    recommended_cameras = Camera.objects.filter(
        available=True,
        film_format=camera.film_format
    ).exclude(
        id=camera.id
    )[:3]

    # If no cameras with the same film format are found, recommend cameras with the same trip type instead.
    if not recommended_cameras:
        recommended_cameras = Camera.objects.filter(
            available=True,
            recommended_trip_type=camera.recommended_trip_type
        ).exclude(
            id=camera.id
        )[:3]

    # Send the selected camera, like status, and recommendations to the template.
    return render(request, "catalogue/camera_detail.html", {
        "camera": camera,
        "user_liked": user_liked,
        "recommended_cameras": recommended_cameras,
    })

def about(request):
    # Display the About page.
    return render(request, "catalogue/about.html")