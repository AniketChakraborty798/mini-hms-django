from django.conf import settings
from django.db import models
from doctors.models import Availability

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    availability = models.OneToOneField(
        Availability,
        on_delete=models.CASCADE
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} -> {self.availability}"
