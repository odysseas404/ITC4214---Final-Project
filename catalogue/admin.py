from django.contrib import admin
from .models import (
    Category,
    Manufacturer,
    Camera,
    CameraImage,
    BorrowRequest,
    CameraLike,
)


class CameraImageInline(admin.TabularInline):
    model = CameraImage
    extra = 1


class CameraAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "manufacturer",
        "category",
        "film_format",
        "condition",
        "available",
    )

    list_filter = (
        "manufacturer",
        "category",
        "film_format",
        "condition",
        "available",
    )

    search_fields = (
        "name",
        "manufacturer__name",
    )

    inlines = [CameraImageInline]


class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "camera",
        "trip_destination",
        "trip_start_date",
        "trip_end_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "trip_start_date",
    )

    search_fields = (
        "user__username",
        "camera__name",
        "trip_destination",
    )


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraImage)
admin.site.register(BorrowRequest, BorrowRequestAdmin)
admin.site.register(CameraLike)