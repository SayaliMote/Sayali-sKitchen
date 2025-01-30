from django import forms
from .models import Reservation

class ReserveTableForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
    STORE_LOCATIONS = (
        ('New York', 'New York'),
        ('Los Angeles', 'Los Angeles'),
        ('Chicago', 'Chicago'),
        ('Houston', 'Houston'),
        ('Phoenix', 'Phoenix'),
        ('Philadelphia', 'Philadelphia'),
        ('San Antonio', 'San Antonio'),
        ('San Diego', 'San Diego'),
        ('Dallas', 'Dallas'),
        ('San Jose', 'San Jose')
    )
    location = forms.ChoiceField(choices=STORE_LOCATIONS)
