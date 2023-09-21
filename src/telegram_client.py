import json
import logging
import os
from dataclasses import dataclass

import requests

BASE_URL = "https://api.telegram.org/bot{token}/{endpoint}"


@dataclass
class TelegramConfig:
    bot_token: str
    chat_id: str


class TelegramBot:
    def __init__(
        self,
        bot_token: str = None,
        chat_id: str = None,
        logger=None,
    ):
        if not bot_token:
            bot_token = os.environ.get("TELEGRAM_API")
            if not bot_token:
                raise ValueError(
                    "Bot token must be provided or set as an environment"
                    " variable."
                )
        if not chat_id:
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            if not chat_id:
                raise ValueError(
                    "Chat ID must be provided or set as an environment"
                    " variable."
                )
        self.config = TelegramConfig(
            bot_token=bot_token,
            chat_id=chat_id,
        )
        logging.info(f"Config: chat_id={chat_id}")

        self.logger = logger or logging.getLogger(__name__)

    def send_message(self, message: str) -> None:
        """
        Sends a message to the specified chat using the bot.
        """
        endpoint = "sendMessage"
        url = BASE_URL.format(token=self.config.bot_token, endpoint=endpoint)
        payload = {"chat_id": self.config.chat_id, "text": message}

        response = requests.post(url, data=payload)
        response_data = response.json()
        self.logger.info(
            f"Telegram Response: \n{json.dumps(response_data, indent=2)}"
        )

        if not response_data.get("ok"):
            raise requests.RequestException(
                f"Telegram API Error: {response_data.get('description')}"
            )


def send_telegram_message(
    message: str, bot_token: str = None, chat_id: str = None, logger=None
) -> None:
    """
    Convenience function to send message to Telegram
    """
    bot = TelegramBot(bot_token, chat_id, logger=logger)
    bot.send_message(message)
