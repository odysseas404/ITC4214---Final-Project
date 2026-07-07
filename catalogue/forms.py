from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
            "trip_destination": forms.TextInput(attrs={
                "placeholder": "Example: Paris, Rome, Athens",
                "required": True,
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


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "First name",
                "required": True,
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Last name",
                "required": True,
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email address",
                "required": True,
            }),
        }


class TravellerRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=15,
        help_text="Maximum 15 characters.",
        widget=forms.TextInput(attrs={
            "placeholder": "Choose a username",
            "maxlength": "15",
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username and len(username) > 15:
            raise forms.ValidationError(
                "Username must be 15 characters or fewer."
            )

        return username