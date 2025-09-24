from django import forms
from .models import Bet

class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = [
            "name",
            "description",
        ]

class DummyForm(forms.Form):
    pass