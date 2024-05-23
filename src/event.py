import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

TICKETS_PREFIX = "Tickets:"
WEBSITE_PREFIX = "Website:"
TEMPLATE_FILE_NAME = "monthly_events_template.txt"

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Dataclass to represent an event."""

    title: str
    location: str
    description: str
    date: str
    start_time: str
    end_time: str
    tickets: Optional[str] = None
    website: Optional[str] = None

    TEMPLATE_PATH = Path(__file__).parent / f"templates/{TEMPLATE_FILE_NAME}"

    def __post_init__(self) -> None:
        required_fields = [
            "title",
            "location",
            "description",
            "date",
            "start_time",
            "end_time",
        ]
        for field_name in required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name.capitalize()} is required.")

        self._parse_description(self.description)

    @property
    def template_content(self) -> str:
        """Lazy-load the template content."""
        if not hasattr(self, "_template_content"):
            self._template_content = self._read_template()
        return self._template_content

    def _read_template(self) -> str:
        """Read the event template file."""
        try:
            with self.TEMPLATE_PATH.open() as template_file:
                return template_file.read()
        except Exception as e:
            logger.error(f"Error reading template file: {e}")
            raise IOError(f"Error reading template file: {e}")

    def _parse_description(self, description: str) -> None:
        """Parse the description to extract extended fields."""
        lines = description.split("\n")
        parsed_lines = []

        for line in lines:
            if line.startswith(TICKETS_PREFIX):
                self.tickets = line.replace(TICKETS_PREFIX, "").strip()
            elif line.startswith(WEBSITE_PREFIX):
                self.website = line.replace(WEBSITE_PREFIX, "").strip()
            else:
                parsed_lines.append(line)

        self.description = "\n".join(parsed_lines).strip()


@dataclass
class EventFormatter:
    @staticmethod
    def format(event: Event) -> str:
        """Pretty print the event using a template."""
        optional_fields = EventFormatter._generate_optional_fields(event)

        return event.template_content.format(
            title=event.title,
            location=event.location,
            description=event.description,
            date=event.date,
            start_time=event.start_time,
            end_time=event.end_time,
            optional_fields=optional_fields,
        ).rstrip()

    @staticmethod
    def _generate_optional_fields(event: Event) -> str:
        """Generate a string of optional fields in markdown format."""
        optional_fields_data = [
            (TICKETS_PREFIX, event.tickets),
            (WEBSITE_PREFIX, event.website),
        ]

        optional_fields = [
            f"[{prefix[:-1]}]({value})"
            for prefix, value in optional_fields_data
            if value
        ]

        return " | ".join(optional_fields) if optional_fields else ""
