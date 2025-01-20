import os
import django
from datetime import timedelta

# Imposta le variabili d'ambiente per Django
os.environ.setdefault('settings', 'django_hill')
django.setup()

from booking.models import Booking
from django.contrib.auth.models import User

def fix_booking_data():
    print("Avvio controllo dati di Booking...")
    bookings_fixed = 0

    for booking in Booking.objects.all():
        # Controlla datetime_start e datetime_end
        if not booking.datetime_start or not booking.datetime_end:
            print(f"Booking {booking.id} ha datetime mancanti!")
            continue

        if booking.datetime_end <= booking.datetime_start:
            print(f"Booking {booking.id} ha datetime incoerenti! Correzione in corso...")
            booking.datetime_end = booking.datetime_start + timedelta(hours=1)
            booking.save()
            bookings_fixed += 1

        # Controlla se il trainer è valido
        if not User.objects.filter(id=booking.trainer_id).exists():
            print(f"Booking {booking.id} ha un trainer_id non valido!")
            continue

    print(f"Controllo completato. Booking corretti: {bookings_fixed}")

if __name__ == "__main__":
    fix_booking_data()
