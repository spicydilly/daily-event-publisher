import logging

from google_calendar_api import get_this_month_events
from telegram_client import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main(credentials_path: str):
    try:
        events = get_this_month_events(credentials_file=credentials_path)

        if not events:
            logger.warning("No events found for this month.")
            return

        messages = [event.pretty() for event in events]
        events_message = "\n\n".join(messages)

        send_telegram_message(events_message, logger=logger)

    except FileNotFoundError:
        logger.error(f"Credentials file '{credentials_path}' not found.")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    # argparse?
    credentials_path = "credentials.json"
    main(credentials_path)
