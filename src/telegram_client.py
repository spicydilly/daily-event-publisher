import json
import logging
import os
from dataclasses import dataclass
from typing import Optional

import requests

BASE_URL = "https://api.telegram.org/bot{token}/{endpoint}"


@dataclass
class TelegramConfig:
    bot_token: str
    chat_id: str


class TelegramBot:
    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.config = TelegramConfig(
            bot_token=bot_token or os.getenv("TELEGRAM_API"),
            chat_id=chat_id or os.getenv("TELEGRAM_CHAT_ID"),
        )
        if not self.config.bot_token:
            raise ValueError(
                "Bot token must be provided or set as an environment variable."
            )
        if not self.config.chat_id:
            raise ValueError(
                "Chat ID must be provided or set as an environment variable."
            )

        self.logger = logger or logging.getLogger(__name__)
        self.logger.info(f"Config: chat_id={self.config.chat_id}")

    def send_message(self, message: str) -> None:
        """
        Sends a message to the specified chat using the bot.

        Args:
            message: The message text to send.
        """
        endpoint = "sendMessage"
        url = BASE_URL.format(token=self.config.bot_token, endpoint=endpoint)
        payload = {
            "chat_id": self.config.chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": "true",
        }

        response = requests.post(url, data=payload)
        response_data = response.json()
        self.logger.info(f"Telegram Response: \n{json.dumps(response_data, indent=2)}")

        if not response_data.get("ok"):
            error_message = response_data.get("description", "Unknown error")
            self.logger.error(f"Telegram API Error: {error_message}")
            raise requests.RequestException(f"Telegram API Error: {error_message}")


def send_telegram_message(
    message: str,
    bot_token: Optional[str] = None,
    chat_id: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> None:
    """
    Convenience function to send a message to Telegram.

    Args:
        message: The message text to send.
        bot_token: The bot token to authenticate the request.
        chat_id: The chat ID to which the message will be sent.
        logger: Optional logger for logging information.

    Returns:
        None
    """
    bot = TelegramBot(bot_token, chat_id, logger=logger)
    bot.send_message(message)
