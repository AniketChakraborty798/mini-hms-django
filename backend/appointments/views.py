from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .calendar_service import GoogleCalendarService

@csrf_exempt
def schedule_appointment(request):
    """
    Example view to schedule an appointment via Google Calendar.
    Expects a POST request with JSON payload containing:
    {
        "summary": "Doctor Appointment",
        "description": "Patient X visit",
        "start_time": "2023-11-20T10:00:00Z",
        "end_time": "2023-11-20T11:00:00Z",
        "attendees": ["patient@example.com"]
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Initialize the Google Calendar Service
            calendar_service = GoogleCalendarService()
            
            if not calendar_service.service:
                return JsonResponse({'error': 'Google Calendar is not configured. Please add credentials.'}, status=500)
                
            event = calendar_service.create_appointment_event(
                summary=data.get('summary', 'Hospital Appointment'),
                description=data.get('description', ''),
                start_time_iso=data.get('start_time'),
                end_time_iso=data.get('end_time'),
                attendees=data.get('attendees')
            )
            
            if event:
                return JsonResponse({
                    'message': 'Appointment scheduled successfully.',
                    'event_link': event.get('htmlLink'),
                    'event_id': event.get('id')
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create appointment in Google Calendar.'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
