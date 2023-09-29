import logging

from event import EventFormatter
from google_calendar_api import get_this_month_events
from telegram_client import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    try:
        events = get_this_month_events()

        if not events:
            logger.warning("No events found for this month.")
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
    main()
