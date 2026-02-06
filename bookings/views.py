from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from doctors.models import Availability
from .models import Booking
import datetime
from .google_calendar import create_calendar_event
import requests
import json


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

    start_dt = datetime.datetime.combine(slot.date, slot.start_time)
    end_dt = datetime.datetime.combine(slot.date, slot.end_time)

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

    # SERVERLESS EMAIL
    trigger_serverless_email(
        patient_email=request.user.email,
        doctor_email=slot.doctor.email
    )

    return redirect('patient-dashboard')

    send_booking_email(
        slot.doctor.email,
        "New Appointment Booked",
        f"You have a new appointment with {request.user.username} on "
        f"{slot.date} from {slot.start_time} to {slot.end_time}."
    )

    return redirect('patient-dashboard')
def trigger_serverless_email(patient_email, doctor_email):
    """
    Calls AWS Lambda (Serverless) to send email
    """
    url = "https://example-api.execute-api.aws/send-email"  # mock URL

    payload = {
        "patient_email": patient_email,
        "doctor_email": doctor_email
    }

    try:
        requests.post(url, json=payload, timeout=2)
    except Exception as e:
        print("Serverless email trigger failed:", e)
