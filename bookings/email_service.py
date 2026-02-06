from django.core.mail import send_mail
from django.conf import settings


def send_booking_confirmation_email(to_email, patient_name, doctor_name):
    subject = "Appointment Confirmation"
    message = (
        f"Hello {patient_name},\n\n"
        f"Your appointment with Dr. {doctor_name} "
        f"has been successfully booked.\n\n"
        "Thank you,\nMini HMS Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
