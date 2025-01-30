from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reserve_table, name='reserve_table'),
    path('confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
]
