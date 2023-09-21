from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Event:
    """Dataclass to represent an event"""

    title: str = field(default=None)
    description: str = field(default=None)
    start_time: str = field(default=None)
    end_time: str = field(default=None)
    tickets: Optional[str] = None
    location: Optional[str] = None
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
        if not self.description:
            raise ValueError("Description is required.")
        if not self.start_time:
            raise ValueError("Start time is required.")
        if not self.end_time:
            raise ValueError("End time is required.")

    def _read_template(self) -> str:
        """Read the event template file."""
        try:
            with self.TEMPLATE_PATH.open() as template_file:
                return template_file.read()
        except Exception as e:
            raise IOError(f"Error reading template file: {e}")

    def pretty(self) -> str:
        """Pretty print the event using a template."""
        optional_fields = [
            f"Tickets: {self.tickets}" if self.tickets else None,
            f"Location: {self.location}" if self.location else None,
            f"Website: {self.website}" if self.website else None,
        ]
        optional_str = " | ".join(filter(None, optional_fields))

        event_pretty = self.template_content.format(
            title=self.title,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time,
            optional_fields=optional_str,
        )

        if optional_str:
            return event_pretty
        # if no optional there is an extra blank line
        return event_pretty[:-1]
