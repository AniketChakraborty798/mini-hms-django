import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

def send_email(to_email, subject, body):
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_pass = os.environ.get("GMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail_user, gmail_pass)
    server.send_message(msg)
    server.quit()


def handler(event, context):
    data = json.loads(event["body"])

    patient_email = data["patient_email"]
    doctor_email = data["doctor_email"]

    send_email(
        patient_email,
        "Appointment Confirmed",
        "Your appointment has been successfully booked."
    )

    send_email(
        doctor_email,
        "New Appointment Booked",
        "A new patient has booked an appointment."
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Emails sent"})
    }
