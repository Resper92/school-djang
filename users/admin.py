from django.contrib import admin
from booking.models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainer', 'user', 'datetime_start', 'datetime_end')
    list_filter = ('trainer', 'datetime_start')
    search_fields = ('trainer__username', 'user__username', 'id')
    ordering = ('-datetime_start',)

    # Controlla se i datetime sono coerenti
    def save_model(self, request, obj, form, change):
        if obj.datetime_end and obj.datetime_start and obj.datetime_end <= obj.datetime_start:
            raise ValueError("La data di fine deve essere successiva alla data di inizio.")
        super().save_model(request, obj, form, change)

admin.site.register(Booking, BookingAdmin)
