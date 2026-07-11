# User is Django's built-in user model, used to connect borrow requests and likes to registered users.
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    # A category can optionally have a parent category, allowing for subcategories.
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories"
    )

    # Controls how the category appears in Django admin and templates.
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Manufacturer(models.Model):
    # The same manufacturer name cannot be saved twice.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        # Manufacturers will be ordered alphabetically.
        ordering = ["name"]

class Camera(models.Model):
    # Fixed choices for camera condition.
    CONDITION_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
    ]

    # Fixed choices for film format.
    FILM_FORMAT_CHOICES = [
        ("35mm", "35mm"),
        ("120", "120"),
        ("Instant", "Instant"),
    ]

    # Fixed choices for the type of trip the camera is recommended for.
    TRIP_TYPE_CHOICES = [
        ("City", "City"),
        ("Nature", "Nature"),
        ("Beach", "Beach"),
        ("Road Trip", "Road Trip"),
        ("Beginner Friendly", "Beginner Friendly"),
        ("Low Light", "Low Light"),
    ]

    # Camera model name, for example: Canon AE-1.
    name = models.CharField(max_length=100)

    # Each camera belongs to one manufacturer; PROTECT means a manufacturer cannot be deleted if cameras still use it.
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT
    )

    # Year the camera was released.
    year = models.PositiveIntegerField()

    # Film format of the camera.
    film_format = models.CharField(
        max_length=20,
        choices=FILM_FORMAT_CHOICES
    )

    # Suggested trip type for this camera.
    recommended_trip_type = models.CharField(
        max_length=50,
        choices=TRIP_TYPE_CHOICES,
        default="Beginner Friendly"
    )

    # Physical condition of the camera.
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="Excellent"
    )

    # Longer description shown on the camera detail page.
    description = models.TextField()

    # Main image of the camera - Uploaded files will be stored inside MEDIA_ROOT/camera_images/.
    main_image = models.ImageField(upload_to="camera_images/")

    # Shows whether the camera can currently be borrowed.
    available = models.BooleanField(default=True)

    # CASCADE means if the category is deleted, its cameras are also deleted.
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class CameraImage(models.Model):
    # Extra gallery images for a camera - related_name="gallery_images" allows access like: camera.gallery_images.all()
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )

    image = models.ImageField(upload_to="camera_gallery/")

    def __str__(self):
        return f"{self.camera.name} Image"

class BorrowRequest(models.Model):
    # Possible statuses for a borrow request.
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Borrowed", "Borrowed"),
        ("Returned", "Returned"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
    ]

    # The user who submitted the borrow request. CASCADE means if the user is deleted, their requests are also deleted.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # The camera requested by the user. PROTECT prevents deleting a camera if it has borrow request history.
    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT
    )

    trip_destination = models.CharField(max_length=150)
    trip_start_date = models.DateField()
    trip_end_date = models.DateField()
    shipping_address = models.TextField()

    # Current status of the request.
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.camera.name} - {self.status}"

class CameraLike(models.Model):
    # The user who liked the camera.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # The camera that was liked.
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents the same user from liking the same camera more than once.
        unique_together = ("user", "camera")

    def __str__(self):
        return f"{self.user.username} likes {self.camera.name}"