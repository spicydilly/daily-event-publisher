import unittest
from unittest.mock import MagicMock, patch

from src.google_calendar_api import Event, GoogleCalendarClient


class TestGoogleCalendarClient(unittest.TestCase):
    @patch("src.google_calendar_api.Credentials.from_service_account_info")
    def setUp(self, mock_from_service_account_info):
        self.gc = GoogleCalendarClient()
        self.mock_service = MagicMock()
        self.gc.service = self.mock_service

    def mock_google_calendar_response(self, items=[]):
        self.mock_service.events().list().execute.return_value = {
            "items": items
        }

    def test_get_events_this_month_no_events(self):
        self.mock_google_calendar_response()

        events = self.gc.get_events_this_month()

        self.assertEqual(events, [])

    def test_get_events_this_month_with_two_events(self):
        mock_response_items = [
            {
                "summary": "Test Event 1",
                "location": "A Place",
                "description": "Description 1",
                "start": {"dateTime": "2023-09-19T10:00:00+01:00"},
                "end": {"dateTime": "2023-09-19T11:00:00+01:00"},
            },
            {
                "summary": "Test Event 2",
                "location": "A Place",
                "description": "Description 2",
                "start": {"dateTime": "2023-09-20T00:00:00+01:00"},
                "end": {"dateTime": "2023-09-20T01:00:00+01:00"},
            },
        ]
        self.mock_google_calendar_response(mock_response_items)

        events = self.gc.get_events_this_month()

        expected_events = [
            Event(
                title="Test Event 1",
                location="A Place",
                description="Description 1",
                date="Sep 19th",
                start_time="10AM",
                end_time="11AM",
            ),
            Event(
                title="Test Event 2",
                location="A Place",
                description="Description 2",
                date="Sep 20th",
                start_time="12AM",
                end_time="1AM",
            ),
        ]
        self.assertEqual(events, expected_events)

    @patch.dict(
        "os.environ", {"GOOGLE_CALENDAR_ID": "", "GOOGLE_CREDENTIALS": ""}
    )
    def test_initialization_without_calendarid_and_credentials(self):
        with self.assertRaises(ValueError) as context:
            self.gcNoEnv = GoogleCalendarClient()
        self.assertTrue(
            "Credentials must be provided or set as an environment variable."
            in str(context.exception)
        )
