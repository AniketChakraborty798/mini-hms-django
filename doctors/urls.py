from django.urls import path
from .views import doctor_dashboard

urlpatterns = [
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),
]
