from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from main.models import Mailing
from main.serializers import ClientSerializer, DetailMailingSerializer, MailingSerializer

User = get_user_model()

server_tz = timezone.get_current_timezone()


class ClientSerializerTest(APITestCase):
    def test_valid_client_serializer(self):
        data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "123",
            "tag": "testtag",
            "timezone": "UTC"
        }

        serializer = ClientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_client_serializer(self):
        data = {
            "phone_number": "invalid",
            "mobile_operator_code": "123",
            "tag": "testtag",
            "timezone": "UTC"
        }

        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)


class MailingSerializerTest(APITestCase):
    def test_valid_mailing_serializer(self):
        data = {
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
            "client_filter": "testtag 123"
        }

        serializer = MailingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_mailing_serializer(self):
        data = {
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
            "client_filter": "invalid_format"
        }

        serializer = MailingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("client_filter", serializer.errors)


class DetailMailingSerializerTest(APITestCase):
    def test_detail_mailing_serializer(self):
        mailing = Mailing.objects.create(start_time="2023-01-01T00:00:00Z", end_time="2023-01-02T00:00:00Z",
                                         message_text="Test message")

        serializer = DetailMailingSerializer(mailing)
        expected_data = {
            "id": mailing.id,
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
            "client_filter": None,
        }

        self.assertEqual(serializer.data, expected_data)
