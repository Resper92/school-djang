from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group

def user_page(request):
    return HttpResponse("Hello, world. You're at the users index.")

def specific_user(request):
    return HttpResponse("Hello, world. You're at the users index.")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"Logged in as: {user.username}")
            return HttpResponse(f"Logged in as: {user.username}")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login/")  
    return redirect("/login/") 

def register_page(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = User.objects.create_user(
            username, password, email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user_group= Group.objects.get(name="Trainer")
        user.groups.add(user_group)
        user.save()
    return render(request, 'register.html')

# Create your views here.
