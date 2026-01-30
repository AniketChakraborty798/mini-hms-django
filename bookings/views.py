from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from doctors.models import Availability
from .models import Booking

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('/')

    slots = Availability.objects.filter(
        is_booked=False
    ).order_by('date', 'start_time')

    return render(request, 'bookings/patient_dashboard.html', {
        'slots': slots
    })


@login_required
def book_slot(request, slot_id):
    if request.user.role != 'patient':
        return redirect('/')

    with transaction.atomic():
        slot = Availability.objects.select_for_update().get(id=slot_id)

        if slot.is_booked:
            return redirect('patient-dashboard')

        slot.is_booked = True
        slot.save()

        Booking.objects.create(
            patient=request.user,
            availability=slot
        )

    return redirect('patient-dashboard')
