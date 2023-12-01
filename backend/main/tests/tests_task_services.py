from unittest.mock import patch

import requests
from django.test import TestCase, override_settings
from django.utils import timezone

from main.models import Client, Mailing, Message
from main.services.task_services import create_message, send_message_and_set_status


class TaskServicesTest(TestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def setUp(self):
        self.client = Client.objects.create(
            phone_number="79991234567",
            mobile_operator_code="123",
            tag="testtag",
            timezone="UTC"
        )
        self.mailing = Mailing.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            message_text="Test message"
        )
        self.message = create_message(
            client_id=self.client.pk,
            mailing_id=self.mailing.pk
        )

    def test_create_message(self):
        self.assertIsInstance(self.message, Message)
        self.assertEqual(self.message.client, self.client)
        self.assertEqual(self.message.mailing, self.mailing)
        self.assertEqual(self.message.status, Message.DELIVERY_IN_PROCESS)

    @patch('main.services.task_services._send_message_to_external_api')
    def test_send_message_and_set_status_success(self, mock_send_message):
        mock_send_message.return_value = 200

        send_message_and_set_status(self.message)

        self.assertEqual(self.message.status, Message.DELIVERED)

    @patch('main.services.task_services._send_message_to_external_api')
    def test_send_message_and_set_status_failure(self, mock_send_message):
        mock_send_message.return_value = 404

        send_message_and_set_status(self.message)

        self.assertEqual(self.message.status, Message.DELIVERY_ERROR)

    @patch('main.services.task_services._send_message_to_external_api')
    def test_send_message_and_set_status_exception(self, mock_send_message):
        mock_send_message.side_effect = requests.RequestException("API call failed")

        send_message_and_set_status(self.message)

        self.assertEqual(self.message.status, Message.DELIVERY_ERROR)
