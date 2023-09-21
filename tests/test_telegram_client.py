import unittest
from unittest.mock import Mock, patch

import requests

from src.telegram_client import TelegramBot


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.bot_token = "TEST_BOT_TOKEN"
        self.chat_id = "TEST_CHAT_ID"
        self.message = "Test message"

    @patch("src.telegram_client.requests.post")
    def test_send_message_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        bot = TelegramBot(self.bot_token, self.chat_id)
        bot.send_message(self.message)

    @patch("src.telegram_client.requests.post")
    def test_send_message_api_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": False,
            "description": "Test API Error",
        }
        mock_post.return_value = mock_response

        bot = TelegramBot(self.bot_token, self.chat_id)

        with self.assertRaises(requests.RequestException) as context:
            bot.send_message(self.message)
        self.assertEqual(
            str(context.exception), "Telegram API Error: Test API Error"
        )

    @patch.dict("os.environ", {"TELEGRAM_API": "", "TELEGRAM_CHAT_ID": ""})
    def test_initialization_without_token_or_chatid(self):
        with self.assertRaises(ValueError) as context:
            self.bot = TelegramBot()
        self.assertTrue(
            "Bot token must be provided or set as an environment variable."
            in str(context.exception)
        )
