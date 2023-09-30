from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

TICKETS_PREFIX = "Tickets:"
WEBSITE_PREFIX = "Website:"


@dataclass
class Event:
    """Dataclass to represent an event"""

    title: str = field(default=None)
    location: str = field(default=None)
    description: str = field(default=None)
    date: str = field(default=None)
    start_time: str = field(default=None)
    end_time: str = field(default=None)
    tickets: Optional[str] = None
    website: Optional[str] = None

    TEMPLATE_PATH = (
        Path(__file__).parent / "templates/monthly_events_template.txt"
    )

    @property
    def template_content(self) -> str:
        if not hasattr(self, "_template_content"):
            self._template_content = self._read_template()
        return self._template_content

    def __post_init__(self):
        if not self.title:
            raise ValueError("Title is required.")
        if not self.location:
            raise ValueError("Location is required.")
        if not self.description:
            raise ValueError("Description is required.")
        if not self.date:
            raise ValueError("Date is required.")
        if not self.start_time:
            raise ValueError("Start time is required.")
        if not self.end_time:
            raise ValueError("End time is required.")
        self._parse_description(self.description)

    def _read_template(self) -> str:
        """Read the event template file."""
        try:
            with self.TEMPLATE_PATH.open() as template_file:
                return template_file.read()
        except Exception as e:
            raise IOError(f"Error reading template file: {e}")

    def _parse_description(self, description: str) -> None:
        """Parse the description to extract extended fields."""
        lines = description.split("\n")

        for line in lines:
            if line.startswith(TICKETS_PREFIX):
                self.tickets = line.replace(TICKETS_PREFIX, "").strip()
            elif line.startswith(WEBSITE_PREFIX):
                self.website = line.replace(WEBSITE_PREFIX, "").strip()

        # Remove extracted details from the main description.
        self.description = "\n".join(
            [
                line
                for line in lines
                if not line.startswith((TICKETS_PREFIX, WEBSITE_PREFIX))
            ]
        ).strip()


@dataclass()
class EventFormatter:
    @staticmethod
    def format(event: Event) -> str:
        """Pretty print the event using a template."""
        # List of optional fields with conditions
        optional_fields_data = [
            (TICKETS_PREFIX, event.tickets),
            (WEBSITE_PREFIX, event.website),
        ]

        # Generate the list of optional fields
        optional_fields = [
            f"[{prefix[:-1]}]({value})"
            for prefix, value in optional_fields_data
            if value
        ]

        # Combine the fields, and add square brackets if there's any content
        optional_str = " | ".join(optional_fields) if optional_fields else ""

        return event.template_content.format(
            title=event.title,
            location=event.location,
            description=event.description,
            date=event.date,
            start_time=event.start_time,
            end_time=event.end_time,
            optional_fields=optional_str,
        ).rstrip()
