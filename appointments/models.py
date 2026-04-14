from django.db import models
from django.conf import settings

class Availability(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'doctor'},
        related_name='availabilities'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
        verbose_name_plural = 'Availabilities'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time}-{self.end_time}"

class Booking(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.availability.is_booked = True
            self.availability.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.pk} by {self.patient.username}"
