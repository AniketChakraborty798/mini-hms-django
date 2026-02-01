from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from doctors.models import Availability
from .models import Booking
import datetime
from .google_calendar import create_calendar_event
from .email_service import send_booking_email

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

    # ---------------------------------
    # BUILD DATETIME OBJECTS
    # ---------------------------------
    start_dt = datetime.datetime.combine(slot.date, slot.start_time)
    end_dt = datetime.datetime.combine(slot.date, slot.end_time)

    # ---------------------------------
    # GOOGLE CALENDAR EVENTS
    # ---------------------------------
    create_calendar_event(
        request.user,
        f"Appointment with Dr. {slot.doctor.username}",
        start_dt,
        end_dt
    )

    create_calendar_event(
        slot.doctor,
        f"Appointment with {request.user.username}",
        start_dt,
        end_dt
    )

    # ---------------------------------
    # EMAIL NOTIFICATIONS
    # ---------------------------------
    send_booking_email(
        request.user.email,
        "Appointment Confirmed",
        f"Your appointment with Dr. {slot.doctor.username} is confirmed on "
        f"{slot.date} from {slot.start_time} to {slot.end_time}."
    )

    send_booking_email(
        slot.doctor.email,
        "New Appointment Booked",
        f"You have a new appointment with {request.user.username} on "
        f"{slot.date} from {slot.start_time} to {slot.end_time}."
    )

    return redirect('patient-dashboard')
