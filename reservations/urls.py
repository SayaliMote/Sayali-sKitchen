from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reserve_table, name='reserve_table'),
    path('seats/<int:branch_id>/', views.seat_selection, name='seat_selection'),
    path('reserve/', views.reserve_seats, name='reserve_seats'),
]
