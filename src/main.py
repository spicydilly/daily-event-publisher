import argparse
import logging

from event import EventFormatter
from google_calendar_api import get_events
from telegram_client import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main(range_type: str):
    try:
        events = get_events(range_type=range_type)

        if not events:
            logger.warning("No events found.")
            return

        messages = []
        for event in events:
            try:
                formatted_event = EventFormatter.format(event)
                messages.append(formatted_event)
            except Exception as format_error:
                logger.error(f"Error formatting event {event}: {format_error}")
                continue  # continue processing other events

        events_message = "\n\n".join(messages)

        send_telegram_message(events_message, logger=logger)

    except Exception as e:
        logger.error(f"Error: {e}")


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
