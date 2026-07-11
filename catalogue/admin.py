# This allows us to register models so they appear in the Django admin panel.
from django.contrib import admin

# Imports the models from this app.
from .models import (
    Category,
    Manufacturer,
    Camera,
    CameraImage,
    BorrowRequest,
    CameraLike,
)


# Allows extra camera images to be added directly inside the Camera admin page.
class CameraImageInline(admin.TabularInline):
    model = CameraImage

    # Shows one empty extra image form by default.
    extra = 1


# Custom admin settings for the Camera model.
class CameraAdmin(admin.ModelAdmin):
    # Fields shown in the camera list page in Django admin.
    list_display = (
        "name",
        "manufacturer",
        "category",
        "film_format",
        "condition",
        "available",
    )

    # Filters shown on the right side of the camera admin page.
    list_filter = (
        "manufacturer",
        "category",
        "film_format",
        "condition",
        "available",
    )

    # Fields that can be searched in the admin search bar.
    search_fields = (
        "name",
        "manufacturer__name",
    )

    # Adds the CameraImageInline inside the Camera admin page.
    inlines = [CameraImageInline]


# Custom admin settings for the BorrowRequest model.
class BorrowRequestAdmin(admin.ModelAdmin):
    # Fields shown in the borrow request list page in Django admin.
    list_display = (
        "user",
        "camera",
        "trip_destination",
        "trip_start_date",
        "trip_end_date",
        "status",
        "created_at",
    )

    # Filters shown on the right side of the borrow request admin page.
    list_filter = (
        "status",
        "trip_start_date",
    )

    # Fields that can be searched in the admin search bar.
    search_fields = (
        "user__username",
        "camera__name",
        "trip_destination",
    )

# Register models so they appear in Django admin.
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraImage)
admin.site.register(BorrowRequest, BorrowRequestAdmin)
admin.site.register(CameraLike)