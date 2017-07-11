from django.forms import ModelForm, HiddenInput
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        labels = {
            'text': 'My Review'
        }