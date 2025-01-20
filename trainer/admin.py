from django.contrib import admin
from .models import Service ,Category,TraineSchedule

class TraineScheduleAdmin(admin.ModelAdmin):
    list_display = ('datatime_start','datatime_end','trainer')
    list_filter = ('trainer',)

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(TraineSchedule,TraineScheduleAdmin)