from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Camera(models.Model):
    name = models.CharField(max_length=100)

    manufacturer = models.CharField(max_length=100)

    description = models.TextField()

    image = models.ImageField(upload_to="camera_images/")

    available = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name