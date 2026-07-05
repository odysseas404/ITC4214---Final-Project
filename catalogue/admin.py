from django.contrib import admin
from .models import Category, Manufacturer, Camera, CameraImage, BorrowRequest 


class CameraImageInline(admin.TabularInline):
    model = CameraImage
    extra = 3


class CameraAdmin(admin.ModelAdmin):
    inlines = [CameraImageInline]


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraImage)
admin.site.register(BorrowRequest)