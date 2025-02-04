from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Branch, Table, Seat, Reservation
from django.utils.timezone import now
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Branch, Table, Seat, Reservation
from django.utils.timezone import now

def reserve_table(request):
    branches = Branch.objects.all()
    return render(request, 'reservations/seat_selection.html', {"branches": branches})

def seat_selection(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    tables = Table.objects.filter(branch=branch)

    data = []
    for table in tables:
        seats = Seat.objects.filter(table=table)
        seat_data = [{"seat_number": seat.seat_number, "is_reserved": seat.is_reserved} for seat in seats]
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

            # Loop through seat IDs and create a reservation for each seat
            for seat_id in seat_ids:
                try:
                    seat = Seat.objects.get(id=seat_id)  # Use the unique ID of the seat
                    if seat.is_reserved:
                        return JsonResponse({"error": f"Seat {seat_id} is already reserved."}, status=400)

                    # Mark the seat as reserved
                    seat.is_reserved = True
                    seat.save()

                    # Create a reservation for the seat
                    Reservation.objects.create(
                        user=request.user if request.user.is_authenticated else None,  # Optional user
                        seat=seat,
                        name=name,
                        phone=phone,
                        email=email,
                        date=date,
                        time=time,
                        number_of_persons=number_of_persons,
                        special_requirements=special_requirements,
                    )
                except Seat.DoesNotExist:
                    return JsonResponse({"error": f"Seat with ID {seat_id} does not exist."}, status=400)

            return JsonResponse({"message": "Seats reserved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request."}, status=400)
