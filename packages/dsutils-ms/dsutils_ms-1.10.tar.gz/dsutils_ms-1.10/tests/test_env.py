from unittest import TestCase

from dsutils_ms.helpers.env import get_credential


class TestEnv(TestCase):
    def test_environment_name(self):
        env_name = get_credential("ENVIRONMENT_NAME")
        self.assertTrue(env_name == "sandbox" or env_name == "production")
