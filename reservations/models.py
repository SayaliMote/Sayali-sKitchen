from django.db import models
from django.forms import ModelForm
from . models import *
# Create your models here.
class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    number_of_persons = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_requirements = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name