from unittest import TestCase

from dsutils_ms.helpers.google_chat import send_message
from dsutils_ms.helpers.env import get_credential


class TestGoogleChat(TestCase):
    def test_google_message(self):
        google_chat = get_credential("WEBHOOK_ALERTAS")
        response = send_message(google_chat, "Pytest - Teste de mensagem")
        self.assertEqual(response.status_code, 200)
