from django import forms
from django.contrib.auth.forms import UserCreationForm


class DateForm(forms.Form):
    startdato = forms.DateField()
    sluttdato = forms.DateField()

    class Meta:
        fields = ["startdato", "sluttdato"]


