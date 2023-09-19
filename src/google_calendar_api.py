import datetime
import json
import logging
import os
from typing import List

from dateutil.relativedelta import relativedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build

from event import Event

# Setup logging
logging.basicConfig(level=logging.INFO)


class GoogleCalendarClient:
    """A class to handle operations related to the Google Calendar."""

    CALENDAR_ID: str = os.environ.get("GOOGLE_CALENDAR_ID", "0")

    def __init__(self, credentials_file: str = None):
        """Initializes the GoogleCalendarClient class with credentials."""
        if not credentials_file:
            credentials_file = os.environ.get(
                "GOOGLE_CALENDAR_CREDENTIALS", "credentials.json"
            )

        self.credentials: Credentials = Credentials.from_service_account_file(
            credentials_file,
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
        )
        self.service: Resource = build(
            "calendar", "v3", credentials=self.credentials
        )

    def get_events_this_month(self) -> List[Event]:
        """Returns the events for the current month in 'Event' format."""
        today = datetime.datetime.utcnow()
        first_day_of_month = today.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        last_day_of_month = (
            first_day_of_month + relativedelta(months=1, days=-1)
        ).replace(hour=23, minute=59, second=59, microsecond=999999)

        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId=self.CALENDAR_ID,
                    timeMin=first_day_of_month.isoformat() + "Z",
                    timeMax=last_day_of_month.isoformat() + "Z",
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            logging.info(
                f"All Events: \n{json.dumps(events_result, indent=2)}"
            )

            events_list: List[Event] = [
                Event(
                    title=event.get("summary", ""),
                    description=event.get("description", ""),
                    start_time=datetime.datetime.fromisoformat(
                        event["start"]
                        .get("dateTime", event["start"].get("date"))
                        .split("Z")[0]
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    end_time=datetime.datetime.fromisoformat(
                        event["end"]
                        .get("dateTime", event["end"].get("date"))
                        .split("Z")[0]
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                )
                for event in events_result.get("items", [])
            ]

            return events_list

        except Exception as e:
            logging.error(f"Error fetching events: {e}")
            return []

    def get_events(self) -> List[Event]:
        """Displays the events for the current month."""
        events = self.get_events_this_month()
        if not events:
            logging.info("No events found for this month.")
        else:
            for event in events:
                logging.info(event)
        return events


if __name__ == "__main__":
    gc = GoogleCalendarClient("credentials.json")
    gc.get_events()
