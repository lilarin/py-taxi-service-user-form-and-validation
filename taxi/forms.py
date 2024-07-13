from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number: str):
    str_part = license_number[:3]
    int_part = license_number[3:]
    if len(license_number) != 8:
        raise ValidationError(
            "License number should consist only of 8 characters"
        )
    elif not str_part.isupper() or not str_part.isalpha():
        raise ValidationError(
            "First 3 characters should be uppercase letters"
        )
    elif not int_part.isdigit():
        raise ValidationError(
            "Last 5 characters should be digits"
        )

    return license_number
