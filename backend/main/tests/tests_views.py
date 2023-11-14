from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Client, Mailing
from main.serializers import ClientSerializer, DetailMailingSerializer, MailingSerializer

User = get_user_model()

server_tz = timezone.get_current_timezone()


class ClientAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.client1 = Client.objects.create(phone_number='12345678901', mobile_operator_code='123', tag='testtag1',
                                             timezone='UTC')
        self.client2 = Client.objects.create(phone_number='98765432101', mobile_operator_code='456', tag='testtag2',
                                             timezone='UTC')

    def test_list_clients(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ClientSerializer(Client.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)


class MailingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.client1 = Client.objects.create(phone_number='12345678901', mobile_operator_code='123', tag='testtag1',
                                             timezone='UTC')
        self.client2 = Client.objects.create(phone_number='98765432101', mobile_operator_code='456', tag='testtag2',
                                             timezone='UTC')

        self.mailing1 = Mailing.objects.create(start_time=datetime.now(server_tz),
                                               end_time=datetime.now(server_tz) + timedelta(days=1),
                                               message_text='Test message 1')
        self.mailing2 = Mailing.objects.create(start_time=datetime.now(server_tz),
                                               end_time=datetime.now(server_tz) + timedelta(days=1),
                                               message_text='Test message 2')

    def test_list_mailings(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('mailing-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = MailingSerializer(Mailing.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_mailing(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('mailing-detail', args=[self.mailing1.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = DetailMailingSerializer(self.mailing1).data
        expected_data['client_filter'] = None

        expected_data = {
            key: expected_data[key] for key in response.data.keys()
        }

        self.assertEqual(response.data, expected_data)
