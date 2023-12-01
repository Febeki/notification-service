import jwt
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from main.models import Client, Mailing, Message
from main.serializers import ClientSerializer, MailingRetrieveSerializer, MailingSerializer, MessageSerializer

User = get_user_model()


class ClientSerializerTest(TestCase):
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

    def test_invalid_phone_number_client_serializer(self):
        data = {
            "phone_number": "invalid",
            "mobile_operator_code": "123",
            "tag": "testtag",
            "timezone": "UTC"
        }

        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['phone_number'])

    def test_invalid_mobile_operator_code_client_serializer(self):
        data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "1234",
            "tag": "testtag",
            "timezone": "UTC"
        }

        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['mobile_operator_code'])

    def test_invalid_tag_client_serializer(self):
        data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "123",
            "tag": "test_tag",
            "timezone": "UTC"
        }

        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['tag'])

    def test_integrity_error_create_client_serializer(self):
        initial_data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "123",
            "tag": "testtag",
            "timezone": "UTC"
        }

        client = ClientSerializer(data=initial_data)
        self.assertTrue(client.is_valid())
        client.save()

        duplicate_data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "456",
            "tag": "testtag",
            "timezone": "UTC"
        }

        duplicate_client = ClientSerializer(data=duplicate_data)
        duplicate_client.is_valid()
        with self.assertRaises(ValidationError):
            duplicate_client.save()

    def test_integrity_error_update_client_serializer(self):
        client1_data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "123",
            "tag": "testtag",
            "timezone": "UTC"
        }

        client2_data = {
            "phone_number": "79990123456",
            "mobile_operator_code": "456",
            "tag": "testtag",
            "timezone": "UTC"
        }

        new_data = {
            "phone_number": "79991234567",
            "mobile_operator_code": "456",
            "tag": "testtag",
            "timezone": "UTC"
        }

        client1 = ClientSerializer(data=client1_data)
        self.assertTrue(client1.is_valid())
        client1.save()

        client2 = ClientSerializer(data=client2_data)
        self.assertTrue(client2.is_valid())
        client2.save()

        update_serializer = ClientSerializer(instance=client2.instance, data=new_data)

        with self.assertRaises(ValidationError):
            update_serializer.is_valid()
            update_serializer.save()


class MailingSerializerTest(TestCase):
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

    def test_invalid_client_filter_mailing_serializer(self):
        data = {
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
            "client_filter": "invalid_format"
        }

        serializer = MailingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['client_filter'])

    def test_invalid_time_mailing_serializer(self):
        data = {
            "start_time": "2023-01-02T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
        }
        serializer = MailingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['non_field_errors'])


class MessageSerializerTest(TestCase):
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

    def test_valid_message_serializer(self):
        data = {
            "status": Message.DELIVERED,
            "mailing": self.mailing.id,
            "client": ClientSerializer(self.client).data
        }

        serializer = MessageSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_mailing_message_serializer(self):
        invalid_data = {
            "status": Message.DELIVERED,
            "mailing": 999,
            "client": ClientSerializer(self.client).data
        }

        serializer = MessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['mailing'])

    def test_invalid_client_message_serializer(self):
        invalid_data = {
            "status": Message.DELIVERED,
            "mailing": self.mailing.id,
            "client": {}
        }

        serializer = MessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors), ['client'])


class MailingRetrieveSerializerTest(TestCase):
    def test_mailing_retrieve_serializer(self):
        mailing = Mailing.objects.create(start_time="2023-01-01T00:00:00Z", end_time="2023-01-02T00:00:00Z",
                                         message_text="Test message")

        serializer = MailingRetrieveSerializer(mailing)
        expected_data = {
            "id": mailing.id,
            "start_time": "2023-01-01T00:00:00Z",
            "end_time": "2023-01-02T00:00:00Z",
            "message_text": "Test message",
            "client_filter": None,
            "messages": [],
        }

        self.assertEqual(serializer.data, expected_data)


class MyTokenObtainPairSerializerTest(APITestCase):
    def setUp(self):
        self.user = self.create_user()

    @staticmethod
    def create_user(username="testuser", password="testpassword"):
        return User.objects.create_user(username=username, password=password)

    def test_obtain_token_with_is_staff(self):
        response = self.client.post(
            "/api/token/",
            data={
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        token_payload = response.data["access"]
        decoded_payload = jwt.decode(token_payload, algorithms=["HS256"], options={"verify_signature": False})
        self.assertIn("is_staff", decoded_payload)
