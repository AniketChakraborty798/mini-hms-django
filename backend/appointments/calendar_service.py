import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()
        
    def _authenticate(self):
        """
        Authenticates the user and returns the Google Calendar service.
        Requires a 'credentials.json' file which can be downloaded from the Google Cloud Console.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    # No credentials file exists, authentication cannot proceed
                    print(f"[{datetime.datetime.now()}] Warning: {self.credentials_path} not found. Google Calendar integration is disabled.")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            return service
        except Exception as error:
            print(f'An error occurred while building the service: {error}')
            return None

    def create_appointment_event(self, summary, description, start_time_iso, end_time_iso, attendees=None):
        """
        Creates an event in the user's primary calendar.
        
        Args:
            summary (str): The title of the appointment.
            description (str): A description of the appointment.
            start_time_iso (str): The start time in ISO 8601 format (e.g. '2023-12-01T09:00:00Z').
            end_time_iso (str): The end time in ISO 8601 format.
            attendees (list of str): A list of email addresses of the attendees.
            
        Returns:
            dict: The created event details containing 'id', 'htmlLink', etc.
        """
        if not self.service:
            print("Google Calendar service is not initialized. Cannot create event.")
            return None
            
        event_body = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time_iso,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time_iso,
                'timeZone': 'UTC',
            },
        }

        if attendees:
             event_body['attendees'] = [{'email': email} for email in attendees]

        try:
            event = self.service.events().insert(
                calendarId='primary', 
                body=event_body,
                sendUpdates='all' # Sends email notifications to attendees
            ).execute()
            
            print(f'Appointment created: {event.get("htmlLink")}')
            return event
        except Exception as error:
            print(f'An error occurred: {error}')
            return None

# Usage Example:
# if __name__ == '__main__':
#     calendar_service = GoogleCalendarService()
#     event = calendar_service.create_appointment_event(
#         summary="Doctor Appointment - Dr. John Doe",
#         description="General Checkup",
#         start_time_iso="2023-11-20T10:00:00Z",
#         end_time_iso="2023-11-20T11:00:00Z",
#         attendees=["patient@example.com"]
#     )
