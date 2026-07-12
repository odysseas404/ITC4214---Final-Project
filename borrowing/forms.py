# Imports timedelta so we can calculate the maximum allowed trip date.
from datetime import timedelta

# Imports Django forms.
from django import forms

# Imports timezone so the form uses Django's current local date.
from django.utils import timezone

# Imports the BorrowRequest model.
from catalogue.models import BorrowRequest


# Form used when a user submits a borrow request.
class BorrowRequestForm(forms.ModelForm):

    class Meta:
        # This form is connected to the BorrowRequest model.
        model = BorrowRequest

        # These are the fields shown to the user in the checkout page.
        fields = [
            "trip_destination",
            "trip_start_date",
            "trip_end_date",
            "shipping_address",
        ]

        # Widgets control how the form fields appear in HTML.
        widgets = {
            "trip_destination": forms.TextInput(attrs={
                "placeholder": "Example: Paris, Rome, Athens",
                "required": True,
                "maxlength": "150",
            }),

            "trip_start_date": forms.DateInput(attrs={
                "type": "date",
                "required": True,
            }),

            "trip_end_date": forms.DateInput(attrs={
                "type": "date",
                "required": True,
            }),

            "shipping_address": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Enter the address where the camera should be shipped",
                "required": True,
                "maxlength": "500",
            }),
        }

    # The __init__ method runs when the form is created.
    # Here we add min and max dates to the date fields for browser validation.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        max_date = today + timedelta(days=30)

        # The trip start date cannot be before today
        # and cannot be more than 30 days from today.
        self.fields["trip_start_date"].widget.attrs["min"] = today.isoformat()
        self.fields["trip_start_date"].widget.attrs["max"] = max_date.isoformat()

        # The trip end date follows the same allowed date range.
        self.fields["trip_end_date"].widget.attrs["min"] = today.isoformat()
        self.fields["trip_end_date"].widget.attrs["max"] = max_date.isoformat()

    # Server-side validation for the trip destination field.
    def clean_trip_destination(self):
        trip_destination = self.cleaned_data.get("trip_destination")

        if not trip_destination:
            raise forms.ValidationError("Trip destination is required.")

        trip_destination = trip_destination.strip()

        if len(trip_destination) < 2:
            raise forms.ValidationError("Trip destination is too short.")

        if len(trip_destination) > 150:
            raise forms.ValidationError("Trip destination is too long.")

        return trip_destination

    # Server-side validation for the shipping address field.
    def clean_shipping_address(self):
        shipping_address = self.cleaned_data.get("shipping_address")

        if not shipping_address:
            raise forms.ValidationError("Shipping address is required.")

        shipping_address = shipping_address.strip()

        if len(shipping_address) < 10:
            raise forms.ValidationError(
                "Please enter a more complete shipping address."
            )

        if len(shipping_address) > 500:
            raise forms.ValidationError("Shipping address is too long.")

        return shipping_address

    # Server-side validation for the date fields.
    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("trip_start_date")
        end = cleaned_data.get("trip_end_date")

        today = timezone.localdate()
        max_date = today + timedelta(days=30)

        # Start date cannot be before today.
        if start and start < today:
            self.add_error(
                "trip_start_date",
                "The trip start date cannot be before today."
            )

        # Start date cannot be later than 30 days from today.
        if start and start > max_date:
            self.add_error(
                "trip_start_date",
                "The trip start date cannot be more than 30 days from today."
            )

        # End date cannot be before today.
        if end and end < today:
            self.add_error(
                "trip_end_date",
                "The trip end date cannot be before today."
            )

        # End date cannot be later than 30 days from today.
        if end and end > max_date:
            self.add_error(
                "trip_end_date",
                "The trip end date cannot be more than 30 days from today."
            )

        # End date cannot be before the start date.
        if start and end and end < start:
            self.add_error(
                "trip_end_date",
                "The trip end date cannot be before the trip start date."
            )

        return cleaned_data