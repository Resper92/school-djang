# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),  # La home page degli utenti
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name='register_page'),
    
    # Dettaglio di un utente specifico
    path('<int:user_id>/', views.specific_user, name='user_specific'),
]
