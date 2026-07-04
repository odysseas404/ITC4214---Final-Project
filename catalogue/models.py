from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
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