from django import forms
from django.contrib.auth.forms import UserCreationForm


class DateForm(forms.Form):
    req_startdate = forms.DateField
    req_sluttdate = forms.DateField
    req_cap = forms.IntegerField()

    class Meta:
        fields = ['req_startdate', 'req_sluttdate', 'req_cap']


class BookingForm(forms.Form):
    req_startdate = forms.DateField
    req_sluttdate = forms.DateField
    req_room_type = forms.CharField

    class Meta2:
        fields = ["req_startdate", "req_sluttdate", "req_room_type"]
