# Imports Django forms.
from django import forms

# Imports Django's built-in User model.
from django.contrib.auth.models import User

# Imports Django's user creation form.
from django.contrib.auth.forms import UserCreationForm


# Form used when a user registers.
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

    # Validates the username during registration.
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username and len(username) > 15:
            raise forms.ValidationError(
                "Username must be 15 characters or fewer."
            )

        return username


# Form used when a logged-in user edits their profile.
class UserUpdateForm(forms.ModelForm):

    # Optional password field.
    # If the user leaves this blank, the password will not change.
    new_password = forms.CharField(
        required=False,
        label="New password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Leave blank to keep current password",
        })
    )

    # Optional password confirmation field.
    confirm_password = forms.CharField(
        required=False,
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat new password",
        })
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Username",
                "required": True,
                "maxlength": "15",
            }),

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

    # Validates the username when the user edits their profile.
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError("Username is required.")

        username = username.strip()

        if len(username) > 15:
            raise forms.ValidationError(
                "Username must be 15 characters or fewer."
            )

        # Prevents the user from choosing a username already used by another account.
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    # Validates the email field.
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Email is required.")

        return email.strip()

    # Validates the optional password change.
    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # If one password field is filled, both must be filled.
        if new_password or confirm_password:

            if not new_password:
                self.add_error(
                    "new_password",
                    "Please enter the new password."
                )

            if not confirm_password:
                self.add_error(
                    "confirm_password",
                    "Please confirm the new password."
                )

            if new_password and confirm_password and new_password != confirm_password:
                self.add_error(
                    "confirm_password",
                    "The passwords do not match."
                )

            if new_password and len(new_password) < 8:
                self.add_error(
                    "new_password",
                    "Password must contain at least 8 characters."
                )

        return cleaned_data