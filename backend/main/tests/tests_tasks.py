import os
from unittest.mock import MagicMock, patch

from django.test import TestCase

from main.models import Message
from main.tasks import send_message_to_client


class CeleryTaskTestCase(TestCase):
    @patch('main.models.Client.objects.get')
    @patch('main.models.Mailing.objects.get')
    @patch('main.models.Message.objects.create')
    @patch('main.tasks.requests.post')
    def test_send_message_to_client_success(self, mock_post, mock_create, mock_get_mailing, mock_get_client):
        client_id = 1
        mailing_id = 2

        mock_get_client.return_value = MagicMock(phone_number='70123456789')
        mock_get_mailing.return_value = MagicMock(message_text='Test message')
        mock_message = MagicMock()
        mock_create.return_value = mock_message

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        send_message_to_client(client_id, mailing_id)

        mock_get_client.assert_called_once_with(id=client_id)
        mock_get_mailing.assert_called_once_with(id=mailing_id)
        mock_create.assert_called_once_with(client=mock_get_client.return_value,
                                            mailing=mock_get_mailing.return_value,
                                            status=Message.DELIVERY_IN_PROCESS)
        mock_post.assert_called_once_with(f'https://probe.fbrq.cloud/v1/send/{mock_message.id}',
                                          json={'id': mock_message.id, 'phone': 70123456789, 'text': 'Test message'},
                                          headers={'Authorization': f'Bearer {os.environ.get("JWT_TOKEN")}'},
                                          timeout=30)
        self.assertEqual(mock_message.status, Message.DELIVERED)
