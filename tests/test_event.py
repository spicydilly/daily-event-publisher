import unittest

from src.event import Event, EventFormatter


class TestEvent(unittest.TestCase):
    def test_missing_title(self):
        with self.assertRaises(TypeError) as context:
            Event(
                description="This is a sample event.",
                location="A Place",
                date="2023-09-26",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(
            str(context.exception),
            "Event.__init__() missing 1 required positional argument: 'title'",
        )

    def test_missing_description(self):
        with self.assertRaises(TypeError) as context:
            Event(
                title="Sample Event",
                location="A Place",
                date="2023-09-26",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(
            str(context.exception),
            "Event.__init__() missing 1 required positional argument: 'description'",
        )

    def test_missing_date(self):
        with self.assertRaises(TypeError) as context:
            Event(
                title="Sample Event",
                location="A Place",
                description="This is a sample event.",
                start_time="10:00",
                end_time="12:00",
            )
        self.assertEqual(
            str(context.exception),
            "Event.__init__() missing 1 required positional argument: 'date'",
        )

    def test_missing_start_time(self):
        with self.assertRaises(TypeError) as context:
            Event(
                title="Sample Event",
                location="A Place",
                date="2023-09-26",
                description="This is a sample event.",
                end_time="12:00",
            )
        self.assertEqual(
            str(context.exception),
            "Event.__init__() missing 1 required positional argument: 'start_time'",
        )

    def test_missing_end_time(self):
        with self.assertRaises(TypeError) as context:
            Event(
                title="Sample Event",
                location="A Place",
                date="2023-09-26",
                description="This is a sample event.",
                start_time="10:00",
            )
        self.assertEqual(
            str(context.exception),
            "Event.__init__() missing 1 required positional argument: 'end_time'",
        )

    def test_pretty_with_mandatory_fields(self):
        event = Event(
            title="Sample Event",
            location="A Place",
            description="This is a sample event.",
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 10:00 to 12:00 @ A Place\n"
            "This is a sample event."
        )
        self.assertEqual(EventFormatter.format(event), expected_output)

    def test_pretty_with_all_fields(self):
        event = Event(
            title="Sample Event",
            location="A Place",
            description=(
                "This is a sample event.\nTickets: www.tickets.com\nWebsite:"
                " www.event-website.com"
            ),
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 10:00 to 12:00 @ A Place\nThis is a"
            " sample event.\n[Tickets](www.tickets.com) |"
            " [Website](www.event-website.com)"
        )
        self.assertEqual(EventFormatter.format(event), expected_output)

    def test_pretty_with_some_optional_fields(self):
        event = Event(
            title="Sample Event",
            location="A Place",
            description="This is a sample event.\nTickets: www.tickets.com",
            date="2023-09-26",
            start_time="10:00",
            end_time="12:00",
        )
        expected_output = (
            "*Sample Event* - 2023-09-26 10:00 to 12:00 @ A Place\n"
            "This is a sample event.\n"
            "[Tickets](www.tickets.com)"
        )
        self.assertEqual(EventFormatter.format(event), expected_output)
