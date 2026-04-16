from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('availability/add/', views.add_availability, name='add_availability'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
]
