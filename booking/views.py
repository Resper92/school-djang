from django.http import HttpResponse
from django.shortcuts import render

def booking_page(request):
    return HttpResponse("Hello, world. You're at the users index.")
def specific_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
def accept_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
def cancel_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
# Create your views here.
