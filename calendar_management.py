import logging
import os
import pickle

import googleapiclient.errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
logger = logging.getLogger('django')


def get_calendar_service():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8050)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_calendar_event(event_name, start_time, end_time):
    service = get_calendar_service()
    event_result = service.events().insert(
        calendarId="primary",
        body={
            "summary": event_name,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Africa/Abidjan"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Africa/Abidjan"},
        }
    ).execute()
    return event_result['id']


def update_calendar_event(event_id, start_time, end_time):
    service = get_calendar_service()
    service.events().patch(
        calendarId="primary",
        eventId=event_id,
        body={
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Africa/Abidjan"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Africa/Abidjan"},
        },
    ).execute()


def delete_calendar_event(event_id):
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id,
        ).execute()
    except googleapiclient.errors.HttpError:
        logger.info(f"Failed to remove an event from calendar (id: {event_id}).")
