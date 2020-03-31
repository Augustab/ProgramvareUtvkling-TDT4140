'''filen med formsene våre'''
from django import forms


class DateForm(forms.Form):
    '''Formen til se tilgjengelige rom etter dato'''
    req_startdate = forms.DateField
    req_sluttdate = forms.DateField
    req_cap = forms.IntegerField()

    class Meta:
        '''Metaklasse'''
        fields = ['req_startdate', 'req_sluttdate', 'req_cap']


class BookingForm(forms.Form):
    '''Formen for bookinger'''
    req_startdate = forms.DateField
    req_sluttdate = forms.DateField
    req_room_type = forms.CharField

    class Meta2:
        '''Metaklasse'''
        fields = ["req_startdate", "req_sluttdate", "req_room_type"]


class CancelForm(forms.Form):
    '''Formen for å slette en booking'''
    bookingid = forms.IntegerField

    class Meta3:
        '''Metaklasse'''
        fields = ["bookingid"]
