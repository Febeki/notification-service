from unittest.mock import Mock, call, patch

from django.test import TestCase, override_settings
from django.utils import timezone

from main.models import Client, Mailing, Message
from main.services.model_services import (
    create_celery_tasks_to_send_messages_to_clients,
    get_clients_by_filter,
    revoke_celery_tasks_by_ids,
)


class ModelServicesTest(TestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def setUp(self):
        self.mailing = Mailing.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            message_text="Test1 message"
        )
        self.client1 = Client.objects.create(
            phone_number="79991234567",
            mobile_operator_code="123",
            tag="tag1",
            timezone="UTC"
        )
        self.client2 = Client.objects.create(
            phone_number="79990123456",
            mobile_operator_code="123",
            tag="tag2",
            timezone="UTC"
        )
        self.client3 = Client.objects.create(
            phone_number="79999012345",
            mobile_operator_code="123",
            tag="tag1",
            timezone="UTC"
        )
        self.message = Message.objects.create(
            status=Message.DELIVERED,
            mailing=self.mailing,
            client=self.client3
        )

    @patch('main.tasks.send_message_to_client.apply_async')
    def test_create_celery_tasks_to_send_messages_to_clients(self, mock_apply_async):
        fake_task_ids = ["1", "2"]
        mock_apply_async.side_effect = lambda args, eta: Mock(id=fake_task_ids.pop(0))
        task_ids = create_celery_tasks_to_send_messages_to_clients(Client.objects.all(), self.mailing)

        self.assertEqual(task_ids, "1,2")

    def test_get_clients_by_filter_with_filter(self):
        client_filter = 'tag1 123'
        filtered_clients = get_clients_by_filter(client_filter)

        self.assertEqual(filtered_clients.count(), 2)

        expected_clients = Client.objects.filter(tag='tag1', mobile_operator_code='123')
        self.assertQuerysetEqual(list(expected_clients), list(filtered_clients))

    def test_get_clients_by_filter_without_filter(self):
        filtered_clients = get_clients_by_filter(None)

        self.assertEqual(filtered_clients.count(), 3)

        all_clients = Client.objects.all()
        for client in all_clients:
            self.assertIn(client, filtered_clients)

    @patch('main.services.model_services.AsyncResult')
    def test_revoke_celery_tasks_by_ids(self, mock_async_result):
        task_ids = ""
        revoke_celery_tasks_by_ids(task_ids)

        mock_async_result.assert_not_called()

        task_ids = "1,2,3"
        revoke_celery_tasks_by_ids(task_ids)

        expected_calls = [call("1"), call("2"), call("3")]
        mock_async_result.assert_has_calls(expected_calls, any_order=True)
