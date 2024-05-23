import unittest
from unittest.mock import patch
from src.main import fetch_and_format_events


class TestFetchAndFormatEvents(unittest.TestCase):

    @patch("main.get_events")
    @patch("main.EventFormatter.format")
    def test_fetch_and_format_events(self, mock_format, mock_get_events):
        mock_get_events.return_value = [{"title": "Event 1"}, {"title": "Event 2"}]
        mock_format.side_effect = lambda x: f"Formatted {x['title']}"

        result = fetch_and_format_events("week")
        self.assertEqual(result, ["Formatted Event 1", "Formatted Event 2"])
