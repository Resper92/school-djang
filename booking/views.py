from django.http import HttpResponse
from django.shortcuts import render, redirect
from booking.models import Booking
from booking.forms  import BookingForm
import trainer.models
from django.contrib.auth.models import User

def booking_page(request):
    if request.method == "GET":
        booking = Booking.objects.filter(user=request.user).all()
        return render(request, "booking_page.html", {"booking": booking})
    

def specific_booking(request,booking_id):
    if request.method == "GET":
        booking = Booking.objects.filter(pk=booking_id).get()
        booking_name = trainer.models.Service.objects.get(pk=booking.service_id).category
        category_name = trainer.models.Category.objects.get(pk=booking_name.id).name
        return render(request, "specific_booking.html", {"booking": booking , "category_name": category_name})
    if request.method == "POST":
        if User is not None:
            booking = Booking.objects.filter(pk=booking_id).get()
            booking.delete()
            return redirect("booking_page")
def accept_booking(request):
    
    return HttpResponse("Hello, world. You're at the users index.")
def cancel_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
# Create your views here.
