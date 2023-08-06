from unittest import TestCase

from dsutils_ms.helpers.datetime import get_timestamp_utc3, get_timestamp_str, get_timestamp_path

from datetime import datetime


class TestDateTime(TestCase):
    def test_datetime_utc3(self):
        utc3 = get_timestamp_utc3()
        self.assertEqual(isinstance(utc3, datetime), True)

    def test_datetime_str(self):
        datetime_str = get_timestamp_str()
        self.assertEqual(isinstance(datetime_str, str), True)

    def test_datetime_path(self):
        datetime_path = get_timestamp_path()
        self.assertEqual(isinstance(datetime_path, str), True)
