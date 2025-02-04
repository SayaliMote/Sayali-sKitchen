from django.contrib import admin
from .models import Branch, Table, Seat, Reservation

# Custom admin configuration for Branch
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')

# Custom admin configuration for Reservation
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'date', 'time', 'number_of_persons', 'seat')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('date', 'time')

# Register models with the admin site
admin.site.register(Branch, BranchAdmin)
admin.site.register(Table)
admin.site.register(Seat)
admin.site.register(Reservation, ReservationAdmin)
