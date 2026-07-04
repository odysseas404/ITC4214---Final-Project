from django.contrib import admin

from .models import CameraImage, Category, Manufacturer, Camera

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Camera)
admin.site.register(CameraImage)