from django.forms import ModelForm
from content.models import Devotional

class DevotionalForm(ModelForm):
    class Meta:
        model = Devotional
        fields = [
            "title",
            "verse_reference",
            "verse_text",
            "message",
            "is_active",
        ]