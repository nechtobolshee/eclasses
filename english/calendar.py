import logging
import os
import pickle

import googleapiclient.errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CalendarManager:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.CREDENTIALS_FILE = 'english/calendar_credentials.json'
        self.logger = logging.getLogger('django')
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None

        if os.path.exists('english/calendar_token.pickle'):
            with open('english/calendar_token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=8050)

            # Save the credentials for the next run
            with open('english/calendar_token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def create_event(self, event_name, start_time, end_time):
        event_result = self.service.events().insert(
            calendarId="primary",
            body={
                "summary": event_name,
                "start": {"dateTime": start_time.isoformat(), "timeZone": "Africa/Abidjan"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "Africa/Abidjan"},
            }
        ).execute()
        return event_result['id']

    def update_event(self, event_id, start_time, end_time):
        self.service.events().patch(
            calendarId="primary",
            eventId=event_id,
            body={
                "start": {"dateTime": start_time.isoformat(), "timeZone": "Africa/Abidjan"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "Africa/Abidjan"},
            },
        ).execute()

    def delete_event(self, event_id):
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id,
            ).execute()
        except googleapiclient.errors.HttpError:
            self.logger.info(f"Failed to remove an event from calendar (id: {event_id}).")
