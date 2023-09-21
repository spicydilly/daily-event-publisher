import logging

from google_calendar_api import get_this_month_events
from telegram_client import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


events = get_this_month_events(credentials_file="credentials.json")

messages = [event.pretty() for event in events]
events_message = "\n\n".join(messages)


try:
    send_telegram_message(events_message, logger=logger)
except Exception as e:
    # Handle error as needed
    print(f"Error: {e}")
