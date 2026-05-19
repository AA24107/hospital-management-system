import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .models import GoogleCredentials


def create_event_for_user(user, event):

    google_creds = GoogleCredentials.objects.get(user=user)

    creds = Credentials(
        token=google_creds.access_token,
        refresh_token=google_creds.refresh_token,
        token_uri=google_creds.token_uri,
        client_id=google_creds.client_id,
        client_secret=google_creds.client_secret,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=creds)

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()