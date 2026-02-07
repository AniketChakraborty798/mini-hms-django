from django.core.mail import send_mail
from django.conf import settings
import requests
import os


# -------------------------------
# NORMAL DJANGO SMTP EMAIL
# -------------------------------
def send_booking_confirmation_email(to_email, patient_name, doctor_name):
    subject = "Appointment Confirmation"
    message = (
        f"Hello {patient_name},\n\n"
        f"Your appointment with Dr. {doctor_name} has been booked.\n\n"
        "Thank you,\nMini HMS Team"
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )


# -------------------------------
# SERVERLESS (AWS LAMBDA) EMAIL
# -------------------------------
def trigger_serverless_email(patient_email, doctor_email):
    """
    Calls AWS Lambda via API Gateway to send emails
    """

    url = getattr(
        settings,
        "SERVERLESS_EMAIL_URL",
        "https://abc123.execute-api.ap-south-1.amazonaws.com/send-email"
    )

    payload = {
        "patient_email": patient_email,
        "doctor_email": doctor_email
    }

    try:
        response = requests.post(url, json=payload, timeout=3)
        response.raise_for_status()
    except Exception as e:
        print("Serverless email trigger failed:", e)
