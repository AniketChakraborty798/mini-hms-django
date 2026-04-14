from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Availability, Booking
from django.utils import timezone
from .utils import send_email_notification
from django.contrib import messages

@login_required
def dashboard(request):
    if request.user.is_doctor():
        return render(request, 'doctor_dashboard.html', {
            'availabilities': request.user.availabilities.all()
        })
    else:
        doctors = Availability.objects.filter(is_booked=False, date__gte=timezone.now().date()).values_list('doctor__username', 'doctor__id').distinct()
        return render(request, 'patient_dashboard.html', {'doctors': set(doctors)})

@login_required
def add_availability(request):
    if not request.user.is_doctor():
        return redirect('/')
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        try:
            Availability.objects.create(
                doctor=request.user,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, "Availability added successfully.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return redirect('/')

@login_required
def book_appointment(request, doctor_id):
    if not request.user.is_patient():
        return redirect('/')
    
    availabilities = Availability.objects.filter(
        doctor_id=doctor_id, 
        is_booked=False, 
        date__gte=timezone.now().date()
    )
    
    if request.method == 'POST':
        availability_id = request.POST.get('availability_id')
        availability = get_object_or_404(Availability, id=availability_id, is_booked=False)
        
        # Simple locking/verification check (in a real prod, use select_for_update)
        booking = Booking.objects.create(patient=request.user, availability=availability)
        
        # Send Email
        send_email_notification(
            'BOOKING_CONFIRMATION',
            request.user.email,
            request.user.username,
            {'doctor_name': availability.doctor.username, 'time_slot': f"{availability.date} {availability.start_time}"}
        )
        
        messages.success(request, f"Successfully booked appointment with Dr. {availability.doctor.username}.")
        return redirect('/')
        
    return render(request, 'book_appointment.html', {'availabilities': availabilities, 'doctor_id': doctor_id})
