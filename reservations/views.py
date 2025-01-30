from django.shortcuts import render, redirect
from .forms import ReserveTableForm
from .models import Reservation

def reserve_table(request):
    if request.method == 'POST':
        reserve_form = ReserveTableForm(request.POST)
        if reserve_form.is_valid():
            # Retrieve the selected location
            location = request.POST.get('location')
            # Save the reservation
            reservation = reserve_form.save(commit=False)
            reservation.location = location
            reservation.save()
            return redirect('reservations:reservation_confirmation', reservation_id=reservation.id)
    else:
        reserve_form = ReserveTableForm()

    context = {'form' : reserve_form}

    return render(request, 'Reservation/reservations.html', context)


def reservation_confirmation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    context = {'reservation': reservation}
    return render(request, 'reservation_confirmation.html', context)