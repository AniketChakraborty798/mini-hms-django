from django.urls import path
from .views import patient_dashboard, book_slot

urlpatterns = [
    path('patient/dashboard/', patient_dashboard, name='patient-dashboard'),
    path('book/<int:slot_id>/', book_slot, name='book-slot'),
]
