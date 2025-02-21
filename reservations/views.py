from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Branch, Table, Seat, Reservation
from django.utils.timezone import now
import json

def reserve_table(request):
    branches = Branch.objects.all()
    return render(request, 'reservations/seat_selection.html', {"branches": branches})

def seat_selection(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    tables = Table.objects.filter(branch=branch)

    data = []
    for table in tables:
        seats = Seat.objects.filter(table=table)
        seat_data = [{"id": seat.id, "seat_number": seat.seat_number, "is_reserved": seat.is_reserved} for seat in seats]

        data.append({
            "table_number": table.table_number,
            "x_position": table.x_position,
            "y_position": table.y_position,
            "seats": seat_data,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def reserve_seats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_ids = data.get('seats', [])
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            date = data.get('date')
            time = data.get('time')
            number_of_persons = data.get('number_of_persons')
            special_requirements = data.get('special_requirements', '')

            if not seat_ids or not name or not phone or not email or not date or not time:
                return JsonResponse({"error": "Missing required fields."}, status=400)

            reservations = []

            for seat_id in seat_ids:
                try:
                    seat = Seat.objects.get(id=seat_id)
                except Seat.DoesNotExist:
                    return JsonResponse({"error": f"Seat with ID {seat_id} does not exist."}, status=404)

                if seat.is_reserved:
                    return JsonResponse({"error": f"Seat {seat.seat_number} on Table {seat.table.table_number} is already reserved."}, status=400)

                # Mark the seat as reserved
                seat.is_reserved = True
                seat.save()

                # Create reservation object
                reservation = Reservation.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    seat=seat,
                    name=name,
                    phone=phone,
                    email=email,
                    date=date,
                    time=time,
                    number_of_persons=number_of_persons,
                    special_requirements=special_requirements,
                )
                reservations.append(reservation)

            # Send confirmation email
            send_reservation_email(email, name, date, time, number_of_persons, seat_ids)

            return JsonResponse({"message": "Seats reserved successfully!", "reservations": [res.id for res in reservations]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request."}, status=400)

def send_reservation_email(user_email, name, date, time, number_of_persons, seats):
    """ Sends a reservation confirmation email """
    subject = "Your Reservation Confirmation"
    context = {
        "name": name,
        "date": date,
        "time": time,
        "seats": seats,
        "number_of_persons": number_of_persons,
    }
    
    html_message = render_to_string("reservations/email_confirmation.html", context)
    send_mail(
        subject,
        "",  # Leave the plain-text version empty since we're using HTML
        settings.EMAIL_HOST_USER,
        [user_email],
        html_message=html_message,
    )
