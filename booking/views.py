from django.http import HttpResponse
from django.shortcuts import render, redirect
from booking.models import Booking
from booking.forms  import BookingForm

def booking_page(request):
    if request.method == "GET":
        booking = Booking.objects.filter(user=request.user).all()
        return render(request, "booking_page.html", {"booking": booking})
    

def specific_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
def accept_booking(request):
    
    return HttpResponse("Hello, world. You're at the users index.")
def cancel_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
# Create your views here.
