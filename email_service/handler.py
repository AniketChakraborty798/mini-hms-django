import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# A mock for the email sending process to see it logging locally
def send_email(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        recipient = body.get('recipient')
        name = body.get('name', 'User')
        
        if not action or not recipient:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "action and recipient are required"})
            }
        
        subject = ""
        message = ""
        
        if action == "SIGNUP_WELCOME":
            subject = "Welcome to Mini HMS!"
            message = f"Hello {name},\n\nWelcome to our Hospital Management System! You have successfully signed up."
        elif action == "BOOKING_CONFIRMATION":
            doctor_name = body.get('doctor_name', 'your doctor')
            time_slot = body.get('time_slot', 'your slot')
            subject = "Appointment Confirmation"
            message = f"Hello {name},\n\nYour appointment with {doctor_name} has been confirmed for {time_slot}."
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Unknown action: {action}"})
            }
        
        # Here we would normally connect to an SMTP server. 
        # For this offline demo, we will just print what would be sent.
        print(f"--- FAKE EMAIL SENT ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Message:\n{message}")
        print(f"-----------------------")
        
        # Uncomment below and add credentials to send real emails
        '''
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "your_email@gmail.com"
        smtp_pass = "your_app_password"
        
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        '''

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully (simulated)",
                "action": action
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
