from django.db import models
from django.conf import settings

class Branch(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Table(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="tables")
    table_number = models.IntegerField()
    capacity = models.IntegerField(default=4)
    x_position = models.IntegerField()
    y_position = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} - {self.branch.name}"

class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} at Table {self.table.table_number}"

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    seat = models.ForeignKey('Seat', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    number_of_persons = models.IntegerField()
    special_requirements = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.name} for Seat {self.seat}"