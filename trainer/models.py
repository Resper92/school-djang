from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class TraineDescription(models.Model):
    text = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    
class TraineSchedule(models.Model):
    datatime_start = models.DateTimeField()
    datatime_end = models.DateTimeField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.trainer.username}: {self.datatime_start} - {self.datatime_end}"
    
class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    level = models.IntegerField()
    duration = models.IntegerField() 