# booking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('booking_page/', views.booking_page, name='booking_page'),  # Pagina delle prenotazioni
    path('<int:booking_id>/', views.specific_booking, name='specific_booking'),  # Dettaglio prenotazione
    path('<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),  # Accetta prenotazione
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),  # Annulla prenotazione
]
