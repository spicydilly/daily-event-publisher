import unittest

from src.event import Event, EventFormatter


class TestEvent(unittest.TestCase):
    def test_missing_title(self):
        with self.assertRaises(ValueError) as context:
            Event(
                description="This is a sample event.",
                date="2023-09-26",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Title is required.")

    def test_missing_description(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                date="2023-09-26",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Description is required.")

    def test_missing_date(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                description="This is a sample event.",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Date is required.")

    def test_missing_start_time(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                date="2023-09-26",
                description="This is a sample event.",
                end_time="12:00",
            )
        self.assertEqual(str(context.exception), "Start time is required.")

    def test_missing_end_time(self):
        with self.assertRaises(ValueError) as context:
            Event(
                title="Sample Event",
                date="2023-09-26",
                description="This is a sample event.",
                start_time="10:00",
            )
        self.assertEqual(str(context.exception), "End time is required.")

    def test_pretty_with_mandatory_fields(self):
        event = Event(
            title="Sample Event",
            description="This is a sample event.",
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 @ 10:00 to 12:00\n"
            "This is a sample event."
        )
        self.assertEqual(EventFormatter.format(event), expected_output)

    def test_pretty_with_all_fields(self):
        event = Event(
            title="Sample Event",
            description=(
                "This is a sample event.\nTickets: www.tickets.com\nLocation:"
                " Main Hall\nWebsite: www.event-website.com"
            ),
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 @ 10:00 to 12:00\nThis is a sample"
            " event.\n[Tickets](www.tickets.com) | [Location](Main Hall) |"
            " [Website](www.event-website.com)"
        )
        self.assertEqual(EventFormatter.format(event), expected_output)

    def test_pretty_with_some_optional_fields(self):
        event = Event(
            title="Sample Event",
            description=(
                "This is a sample event.\nTickets: www.tickets.com\nLocation:"
                " Main Hall"
            ),
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 @ 10:00 to 12:00\n"
            "This is a sample event.\n"
            "[Tickets](www.tickets.com) | [Location](Main Hall)"
        )
        self.assertEqual(EventFormatter.format(event), expected_output)


if __name__ == "__main__":
    unittest.main()
