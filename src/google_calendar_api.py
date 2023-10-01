import json
import logging
import os
from datetime import datetime, timedelta
from typing import List

from dateutil.relativedelta import relativedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build

from event import Event


class GoogleCalendarClient:
    """A class to handle operations related to the Google Calendar."""

    SERVICE_NAME = "calendar"
    SERVICE_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(
        self,
        credentials: str = None,
        calendar_id: str = None,
        logger=None,
    ):
        """Initializes the GoogleCalendarClient class with credentials."""

        if not credentials:
            credentials = os.environ.get("GOOGLE_CREDENTIALS")
            if not credentials:
                raise ValueError(
                    "Credentials must be provided or set as an environment"
                    " variable."
                )

        if not calendar_id:
            calendar_id = os.environ.get("GOOGLE_CALENDAR_ID")
            if not calendar_id:
                raise ValueError(
                    "Calendar ID must be provided or set as an environment"
                    " variable."
                )

        self.calendar_id = calendar_id

        self.credentials: Credentials = Credentials.from_service_account_info(
            json.loads(credentials)
        )

        self.service: Resource = build(
            self.SERVICE_NAME,
            self.SERVICE_VERSION,
            credentials=self.credentials,
        )

        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def determine_date_range(range_type: str = "month") -> tuple():
        """
        Determines the date range to fetch events for.
        :param range_type: 'month' or 'week' to specify the desired date range.
        """
        if range_type not in ["month", "week"]:
            raise ValueError("range_type must be either 'month' or 'week'")

        today = datetime.utcnow()
        if range_type == "month":
            start_date = today.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            end_date = (start_date + relativedelta(months=1, days=-1)).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        else:
            days_until_tuesday = (
                1 - today.weekday() + 7
            ) % 7  # 1 represents Tuesday
            start_date = (today + timedelta(days=days_until_tuesday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            days_until_next_monday = (
                0 - today.weekday() + 7
            ) % 7 + 7  # 0 represents Monday
            end_date = (
                today + timedelta(days=days_until_next_monday)
            ).replace(hour=23, minute=59, second=59, microsecond=999999)
        return (start_date.isoformat() + "Z", end_date.isoformat() + "Z")

    def get_events(self, range_type: str = "month") -> List[Event]:
        """
        Returns the events for the specified date range in 'Event' format.
        :param range_type: 'month' or 'week' to specify the desired date range.
        """
        date_range = self.determine_date_range(range_type)
        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=date_range[0],
                    timeMax=date_range[1],
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            self.logger.info(
                f"All Events: \n{json.dumps(events_result, indent=2)}"
            )

            events_list: List[Event] = [
                Event(
                    title=event.get("summary", ""),
                    location=event.get("location", ""),
                    description=event.get("description", ""),
                    start_time=self.get_date(event["start"])
                    .strftime("%I%p")
                    .lstrip("0"),
                    date=(
                        f"{self.get_date(event['start']).strftime('%b')} "
                        f"{self.ordinal(self.get_date(event['start']).day)}"
                    ),
                    end_time=self.get_date(event["end"])
                    .strftime("%I%p")
                    .lstrip("0"),
                )
                for event in events_result.get("items", [])
            ]

            return events_list
        except Exception as e:
            self.logger.error(f"Error fetching events: {e}")
            return []

    @staticmethod
    def get_date(data):
        return datetime.fromisoformat(
            data.get("dateTime", data.get("date")).split("Z")[0]
        )

    @staticmethod
    def ordinal(n) -> str:
        """Return number n with an ordinal string suffix."""
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"


def get_events(
    credentials: str = None,
    calendar_id: str = None,
    logger=None,
    range_type: str = "month",
) -> List[Event]:
    """
    Convenience function to fetch events for the current month.
    """
    client = GoogleCalendarClient(
        credentials=credentials,
        calendar_id=calendar_id,
        logger=logger,
    )
    return client.get_events(range_type=range_type)
