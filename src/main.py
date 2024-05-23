import argparse
import logging
from typing import List

from event import EventFormatter
from google_calendar_api import get_events
from telegram_client import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_and_format_events(range_type: str) -> List[str]:
    """
    Fetch events from Google Calendar and format them.

    Args:
        range_type: 'week' or 'month' to specify the desired date range.

    Returns:
        A list of formatted event strings.
    """
    try:
        events = get_events(range_type=range_type)
        if not events:
            logger.warning("No events found.")
            return []

        formatted_events = []
        for event in events:
            try:
                formatted_event = EventFormatter.format(event)
                formatted_events.append(formatted_event)
            except Exception as format_error:
                logger.error(f"Error formatting event {event}: {format_error}")

        return formatted_events

    except ConnectionError:
        logger.error("Network error occurred while fetching events.")
        return []
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return []


def send_events_message(formatted_events: List[str]) -> None:
    """
    Send formatted events as a message via Telegram.

    Args:
        formatted_events: A list of formatted event strings.

    Returns:
        None
    """
    if not formatted_events:
        logger.info("No formatted events to send.")
        return

    events_message = "\n\n".join(formatted_events)
    try:
        send_telegram_message(events_message, logger=logger)
    except Exception as e:
        logger.error(f"Error sending message: {e}")


def main(range_type: str) -> None:
    """
    Main function to fetch and send Google Calendar events.

    Args:
        range_type: 'week' or 'month' to specify the desired date range.

    Returns
        None
    """
    formatted_events = fetch_and_format_events(range_type)
    send_events_message(formatted_events)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch Google Calendar events and send them via Telegram."
    )
    parser.add_argument(
        "--range-type",
        type=str,
        choices=["week", "month"],
        default="month",
        help=(
            "Specify whether to fetch events for the week or the month."
            " Defaults to month."
        ),
    )
    args = parser.parse_args()
    main(range_type=args.range_type)
