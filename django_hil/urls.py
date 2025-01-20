from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from booking import views as booking_views
from trainer import views as trainer_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', user_views.home_page, name='home_page'),  # Home page visibile al primo accesso

    # Includiamo gli URL di ciascuna app
    path('user/', include('users.urls')),  # Gli URL per gli utenti, li definisci in users/urls.py
    path('booking/', include('booking.urls')),  # Gli URL per le prenotazioni
    path('trainer/', include('trainer.urls')),  # Gli URL per i trainer

    # Altri URL generali
    path('login/', user_views.login_page, name='login_page'),
    path('logout/', user_views.logout_page, name='logout_page'),
    path('register/', user_views.register_page, name='register_page'),
]
