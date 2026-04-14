import requests
import threading

def _send_email_async(data):
    try:
        requests.post('http://localhost:4000/email/send', json=data, timeout=5)
    except Exception as e:
        print("Failed to send email:", e)

def send_email_notification(action, email, name, extra_data=None):
    if extra_data is None:
        extra_data = {}
    
    data = {
        'action': action,
        'recipient': email,
        'name': name
    }
    data.update(extra_data)

    thread = threading.Thread(target=_send_email_async, args=(data,))
    thread.start()
