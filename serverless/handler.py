import json
import smtplib
from email.message import EmailMessage
import os

def send_email(event, context):
    body = json.loads(event["body"])

    patient_email = body["patient_email"]
    doctor_email = body["doctor_email"]

    msg = EmailMessage()
    msg["Subject"] = "Appointment Confirmation"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = patient_email
    msg.set_content(
        f"Your appointment is confirmed.\nDoctor email: {doctor_email}"
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASS"]
        )
        server.send_message(msg)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email sent"})
    }
