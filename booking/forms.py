from django import forms
from django.contrib.auth.models import User
from .models import Booking

class BookingForm(forms.Form):
    service = forms.CharField(max_length=100)
    datetime_start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    datetime_end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )