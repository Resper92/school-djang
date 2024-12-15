from django.http import HttpResponse, request
from django.shortcuts import render

def user_page(request):
    return HttpResponse("Hello, world. You're at the users index.")

def specific_user(request):
    return HttpResponse("Hello, world. You're at the users index.")

def login_page(request):
    return HttpResponse("Hello, world. You're at the users index.")

def logout_page(request):
    return HttpResponse("Hello, world. You're at the users index.")

def register_page(request):
    return HttpResponse("Hello, world. You're at the users index.")

# Create your views here.
