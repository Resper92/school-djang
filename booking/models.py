from django.contrib.auth.models import User 
from django.db import models

from trainer.models import Service  

class Booking (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", unique=False)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainings", unique=False)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staatus= models.BooleanField(default=False)