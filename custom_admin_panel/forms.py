# Imports Django forms.
from django import forms

# Imports the Camera model from the catalogue app.
from catalogue.models import Camera

# Form used by the Catalogue Manager to add a new camera listing.
class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera

        fields = [
            "name",
            "manufacturer",
            "year",
            "film_format",
            "recommended_trip_type",
            "condition",
            "description",
            "main_image",
            "available",
            "category",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Example: Canon AE-1",
                "required": True,
            }),
            "year": forms.NumberInput(attrs={
                "placeholder": "Example: 1976",
                "required": True,
            }),
            "description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write a short description of the camera.",
                "required": True,
            }),
        }