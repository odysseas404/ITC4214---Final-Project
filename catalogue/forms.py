from django import forms
from .models import BorrowRequest


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = [
            "trip_destination",
            "trip_start_date",
            "trip_end_date",
            "shipping_address",
        ]

        widgets = {
            "trip_start_date": forms.DateInput(attrs={
                "type": "date",
                "required": True,
            }),
            "trip_end_date": forms.DateInput(attrs={
                "type": "date",
                "required": True,
            }),
            "trip_destination": forms.TextInput(attrs={
                "placeholder": "Example: Paris, Rome, Athens",
                "required": True,
            }),
            "shipping_address": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Enter the address where the camera should be shipped",
                "required": True,
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("trip_start_date")
        end = cleaned_data.get("trip_end_date")

        if start and end and end < start:
            raise forms.ValidationError(
                "The return date cannot be before the trip start date."
            )

        return cleaned_data