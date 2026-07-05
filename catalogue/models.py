from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories"
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Camera(models.Model):

    CONDITION_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
    ]

    FILM_FORMAT_CHOICES = [
        ("35mm", "35mm"),
        ("120", "120"),
        ("Instant", "Instant"),
    ]

    name = models.CharField(max_length=100)

    manufacturer = models.ForeignKey(
    Manufacturer,
    on_delete=models.PROTECT
    )

    year = models.PositiveIntegerField()

    film_format = models.CharField(
        max_length=20,
        choices=FILM_FORMAT_CHOICES
    )

    TRIP_TYPE_CHOICES = [
    ("City", "City"),
    ("Nature", "Nature"),
    ("Beach", "Beach"),
    ("Road Trip", "Road Trip"),
    ("Beginner Friendly", "Beginner Friendly"),
    ("Low Light", "Low Light"),
    ]

    recommended_trip_type = models.CharField(
    max_length=50,
    choices=TRIP_TYPE_CHOICES,
    default="Beginner Friendly"
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="Excellent"
    )

    description = models.TextField()

    main_image = models.ImageField(upload_to="camera_images/")

    available = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class CameraImage(models.Model):
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )

    image = models.ImageField(
        upload_to="camera_gallery/"
    )

    def __str__(self):
        return f"{self.camera.name} Image"
    
class BorrowRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Borrowed", "Borrowed"),
        ("Returned", "Returned"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT
    )

    trip_destination = models.CharField(max_length=150)

    trip_start_date = models.DateField()

    trip_end_date = models.DateField()

    shipping_address = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.camera.name} - {self.status}"
    
class CameraLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "camera")

    def __str__(self):
        return f"{self.user.username} likes {self.camera.name}"