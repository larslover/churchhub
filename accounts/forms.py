from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .phone_utils import COUNTRY_CODES


class CustomUserCreationForm(UserCreationForm):

    country_code = forms.ChoiceField(
        choices=COUNTRY_CODES,
        initial="+91",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    local_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter mobile number"
        })
    )
    def save(self, commit=True):
        user = super().save(commit=False)

        country_code = self.cleaned_data["country_code"]
        local_phone = self.cleaned_data["local_phone"]

        user.phone = f"{country_code}{local_phone}"

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ("full_name", "email")