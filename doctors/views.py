from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Availability

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('/')

    if request.method == 'POST':
        Availability.objects.create(
            doctor=request.user,
            date=request.POST['date'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time']
        )
        return redirect('doctor-dashboard')

    slots = Availability.objects.filter(doctor=request.user).order_by('date', 'start_time')

    return render(request, 'doctors/doctor_dashboard.html', {
        'slots': slots
    })
