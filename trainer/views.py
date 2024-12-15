from django.http import HttpResponse
from django.shortcuts import render

def trainer_page(request):
    return HttpResponse("Hello, world. You're at the users index.")
def category_page(request):
    return HttpResponse("Hello, world. You're at the users index.")
def specific_trainer(request):
    return HttpResponse("Hello, world. You're at the users index.")
def trainer_service(request):
    return HttpResponse("Hello, world. You're at the users index.")
def trainer_service_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")
# Create your views here.
