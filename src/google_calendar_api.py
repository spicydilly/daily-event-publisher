import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Tuple, Optional

from dateutil.relativedelta import relativedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from event import Event


class GoogleCalendarClient:
    """A class to handle operations related to the Google Calendar."""

    SERVICE_NAME = "calendar"
    SERVICE_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    ERROR_CREDENTIALS = (
        "Credentials must be provided or set as an environment variable."
    )
    ERROR_CALENDAR_ID = (
        "Calendar ID must be provided or set as an environment variable."
    )
    ERROR_RANGE_TYPE = "range_type must be either 'month' or 'week'."

    def __init__(
        self,
        credentials: Optional[str] = None,
        calendar_id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """Initializes the GoogleCalendarClient class with credentials."""
        credentials = credentials or os.getenv("GOOGLE_CREDENTIALS")
        if not credentials:
            raise ValueError(self.ERROR_CREDENTIALS)

        calendar_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID")
        if not calendar_id:
            raise ValueError(self.ERROR_CALENDAR_ID)

        self.calendar_id = calendar_id
        self.credentials = Credentials.from_service_account_info(
            json.loads(credentials)
        )
        self.service = build(
            self.SERVICE_NAME, self.SERVICE_VERSION, credentials=self.credentials
        )
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def determine_date_range(range_type: str = "month") -> Tuple[str, str]:
        """
        Determines the date range to fetch events for.

        Args:
            range_type: 'month' or 'week' to specify the desired date range.

        Returns:
            A tuple of start and end date strings in ISO format with 'Z' suffix.
        """
        if range_type not in {"month", "week"}:
            raise ValueError(GoogleCalendarClient.ERROR_RANGE_TYPE)

        today = datetime.now(timezone.utc)
        if range_type == "month":
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + relativedelta(months=1)).replace(
                day=1
            ) - timedelta(seconds=1)
        else:
            start_date = today - timedelta(
                days=today.weekday()
            )  # Start of the current week (Monday)
            end_date = start_date + timedelta(
                days=6, hours=23, minutes=59, seconds=59, microseconds=999999
            )

        return start_date.isoformat() + "Z", end_date.isoformat() + "Z"

    def get_events(self, range_type: str = "month") -> List[Event]:
        """
        Returns the events for the specified date range in 'Event' format.

        Args:
            range_type: 'month' or 'week' to specify the desired date range.

        Returns:
            A list of Event objects.
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
            self.logger.info(f"All Events: \n{json.dumps(events_result, indent=2)}")

            events_list = [
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
                    end_time=self.get_date(event["end"]).strftime("%I%p").lstrip("0"),
                )
                for event in events_result.get("items", [])
            ]

            return events_list
        except Exception as e:
            self.logger.error(f"Error fetching events: {e}")
            return []

    @staticmethod
    def get_date(data: dict) -> datetime:
        """
        Extracts the date from the event data.

        Args:
            A dictionary containing event date information.

        Returns:
            A datetime object.
        """
        return datetime.fromisoformat(
            data.get("dateTime", data.get("date")).split("Z")[0]
        )

    @staticmethod
    def ordinal(n: int) -> str:
        """Return number n with an ordinal string suffix."""
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"


def get_events(
    credentials: Optional[str] = None,
    calendar_id: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    range_type: str = "month",
) -> List[Event]:
    """
    Convenience function to fetch events for the specified date range.
    :param credentials: Google API credentials in JSON format.
    :param calendar_id: Google Calendar ID.
    :param logger: Logger instance for logging information.
    :param range_type: 'month' or 'week' to specify the desired date range.
    :return: A list of Event objects.
    """
    client = GoogleCalendarClient(
        credentials=credentials, calendar_id=calendar_id, logger=logger
    )
    return client.get_events(range_type=range_type)
