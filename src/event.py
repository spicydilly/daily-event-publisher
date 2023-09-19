from dataclasses import dataclass, field
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

    def __post_init__(self):
        if not self.title:
            raise ValueError("Title is required.")
        if not self.description:
            raise ValueError("Description is required.")
        if not self.start_time:
            raise ValueError("Start time is required.")
        if not self.end_time:
            raise ValueError("End time is required.")

    def pretty(self) -> str:
        """Pretty print the event."""
        base_str = (
            f"Event: {self.title}\n"
            f"Description: {self.description}\n"
            f"Starts: {self.start_time} - Ends: {self.end_time}"
        )

        additional_str = []
        if self.tickets:
            additional_str.append(f"Tickets: {self.tickets}")
        if self.location:
            additional_str.append(f"Location: {self.location}")
        if self.website:
            additional_str.append(f"Website: {self.website}")

        optional_str = " | ".join(additional_str)

        if optional_str:
            return f"{base_str}\n{optional_str}"
        else:
            return base_str
