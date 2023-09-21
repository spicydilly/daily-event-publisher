import unittest

from src.event import Event


class TestEvent(unittest.TestCase):
    def test_pretty_with_mandatory_fields(self):
        event = Event(
            "Sample Event", "This is a sample event.", "10:00", "12:00"
        )
        expected_output = (
            "Event: Sample Event\n"
            "Description: This is a sample event.\n"
            "Starts: 10:00 - Ends: 12:00\n"
        )
        self.assertEqual(event.pretty(), expected_output)

    def test_pretty_with_all_fields(self):
        event = Event(
            "Sample Event",
            "This is a sample event.",
            "10:00",
            "12:00",
            "www.tickets.com",
            "Main Hall",
            "www.event-website.com",
        )
        expected_output = (
            "Event: Sample Event\nDescription: This is a sample"
            " event.\nStarts: 10:00 - Ends: 12:00\nTickets: www.tickets.com |"
            " Location: Main Hall | Website: www.event-website.com\n"
        )
        self.assertEqual(event.pretty(), expected_output)

    def test_pretty_with_some_optional_fields(self):
        event = Event(
            "Sample Event",
            "This is a sample event.",
            "10:00",
            "12:00",
            "www.tickets.com",
            "Main Hall",
        )
        expected_output = (
            "Event: Sample Event\n"
            "Description: This is a sample event.\n"
            "Starts: 10:00 - Ends: 12:00\n"
            "Tickets: www.tickets.com | Location: Main Hall\n"
        )
        self.assertEqual(event.pretty(), expected_output)

    def test_missing_title(self):
        with self.assertRaises(ValueError) as context:
            Event(
                description="This is a sample event.",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Title is required.")

    def test_missing_description(self):
        with self.assertRaises(ValueError) as context:
            Event(title="Sample Event", start_time="10:00", end_time="12:00")
        self.assertEqual(str(context.exception), "Description is required.")

    def test_missing_start_time(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                description="This is a sample event.",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Start time is required.")

    def test_missing_end_time(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                description="This is a sample event.",
                start_time="10:00",
            )
        self.assertEqual(str(context.exception), "End time is required.")


if __name__ == "__main__":
    unittest.main()
