from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from users.forms import loginForm ,registerForm,userForm


def home_page(request):
    return render(request, "home.html")

@login_required
def user_page(request):
    user = request.user
    return render(request, "user.html", {"user": user})
    


def specific_user(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return HttpResponse("Utente non trovato", status=404)

    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('user_specific', user_id=user.id)
    else: 
        form = userForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

    return render(request, 'user_detail.html', {'form': form, 'user': user})


def login_page(request):
    if request.method == 'GET':
        form = loginForm()
        return render(request, 'login.html', context={'form': form})
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid(): 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
        # Se le credenziali non sono corrette, rimanda alla stessa pagina di login
        return redirect('login_page')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login/")  
    return redirect("/login/") 

def register_page(request):
    if request.method == 'GET':
        form = registerForm()
        return render(request, 'register.html', {'form': form})

    form = registerForm(request.POST)
    if form.is_valid():
        created_user = form.save()
        client_group, _ = Group.objects.get_or_create(name="user")
        created_user.groups.add(client_group)
        created_user.save()
        return redirect('login_page')

    # 🚨 Assicurati di restituire il form con errori
    return render(request, 'register.html', {'form': form}, status=400)
