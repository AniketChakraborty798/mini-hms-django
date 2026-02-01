from django.urls import path
from . import views

urlpatterns = [
    path(
        'patient/dashboard/',
        views.patient_dashboard,
        name='patient-dashboard'
    ),

    path(
        'patient/book/<int:slot_id>/',
        views.book_slot,
        name='book-slot'
    ),
]
