from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from main.utils import time_to_send_message


class UtilsTestCase(TestCase):
    def setUp(self):
        self.valid_timezone = "Europe/Moscow"
        self.invalid_timezone = "Check/12345"
        self.server_tz = timezone.get_current_timezone()

    def test_time_to_send_message_invalid_timezone(self):
        start_time = datetime.now(self.server_tz) + timedelta(hours=1)
        end_time = datetime.now(self.server_tz) + timedelta(hours=2)
        result = time_to_send_message(self.invalid_timezone, start_time, end_time)
        self.assertIsNone(result)

    def test_time_to_send_message_reverse_time_range(self):
        start_time = datetime.now(self.server_tz) + timedelta(hours=2)
        end_time = datetime.now(self.server_tz) + timedelta(hours=1)
        result = time_to_send_message(self.valid_timezone, start_time, end_time)
        self.assertIsNone(result)

    def test_time_to_send_message_within_time_range(self):
        start_time = datetime.now(self.server_tz) - timedelta(hours=12)
        end_time = datetime.now(self.server_tz) + timedelta(hours=12)
        result = time_to_send_message(self.valid_timezone, start_time, end_time)
        self.assertIsNotNone(result)
