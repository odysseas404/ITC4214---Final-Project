from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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