from django import forms
from django.contrib.auth.forms import UserCreationForm


class DateForm(forms.Form):
    req_startdato = forms.DateField()
    req_sluttdato = forms.DateField()
    req_cap = forms.IntegerField()

    class Meta:
        fields = ["req_startdato", "req_sluttdato", "req_cap"]


class BestillForm(forms.Form):
    req_startdato = forms.DateField()
    req_sluttdato = forms.DateField()
    req_cap = forms.IntegerField()
    req_roomType = forms.CharField()

    class Meta:
        fields = ["req_startdato", "req_sluttdato", "req_cap", "req_roomType"]
