from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .phone_utils import COUNTRY_CODES


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email (optional)"
        })
    )

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

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter full name"
        })
    )

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "country_code",
            "local_phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return None
        return email.lower().strip()

    def validate_unique(self):
        """
        Skip unique email validation when email is blank.
        """
        exclude = self._get_validation_exclusions()

        if not self.cleaned_data.get("email"):
            exclude.add("email")

        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError as e:
            self._update_errors(e)

    def save(self, commit=True):
        user = super().save(commit=False)

        country_code = self.cleaned_data["country_code"]
        local_phone = self.cleaned_data["local_phone"].replace(" ", "").replace("-", "")
        user.phone = f"{country_code}{local_phone}"

        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()

        return user