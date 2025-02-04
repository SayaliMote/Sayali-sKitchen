from django import forms
from .models import Reservation, Table, Seat

class ReserveTableForm(forms.ModelForm):
    table = forms.ModelChoiceField(queryset=Table.objects.all(), required=True)
    seats = forms.ModelMultipleChoiceField(queryset=Seat.objects.filter(is_reserved=False), required=True, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'number_of_persons', 'date', 'time', 'special_requirements', 'table', 'seats']
