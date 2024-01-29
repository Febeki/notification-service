from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Client, Mailing
from main.serializers import ClientSerializer, MailingSerializer

User = get_user_model()

server_tz = timezone.get_current_timezone()


class ClientAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')

        self.test_client = Client.objects.create(phone_number='72345678901', mobile_operator_code='123', tag='testtag1',
                                                 timezone='UTC')
        self.client.force_authenticate(user=self.user)

    def test_list_clients(self):
        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ClientSerializer(Client.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_client(self):
        response = self.client.get(reverse('clients-detail', args=[self.test_client.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.test_client.phone_number)

    def test_patch_client(self):
        data = {'tag': 'NewTag'}
        response = self.client.patch(reverse('clients-detail', args=[self.test_client.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tag'], 'NewTag')

    def test_put_client(self):
        data = {'phone_number': '72345678911', 'mobile_operator_code': '789', 'tag': 'NewTag2', 'timezone': 'UTC'}
        response = self.client.put(reverse('clients-detail', args=[self.test_client.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '72345678911')
        self.assertEqual(response.data['mobile_operator_code'], '789')
        self.assertEqual(response.data['tag'], 'NewTag2')

    def test_delete_client(self):
        response = self.client.delete(reverse('clients-detail', args=[self.test_client.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(pk=self.test_client.pk).exists())

    def test_create_client(self):
        data = {'phone_number': '71111111111', 'mobile_operator_code': '111', 'tag': 'Tag', 'timezone': 'UTC'}
        response = self.client.post(reverse('clients-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tag'], 'Tag')


class MailingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')

        self.mailing1 = Mailing.objects.create(start_time=datetime.now(server_tz),
                                               end_time=datetime.now(server_tz) + timedelta(days=1),
                                               message_text='Test message 1')
        self.mailing2 = Mailing.objects.create(start_time=datetime.now(server_tz),
                                               end_time=datetime.now(server_tz) + timedelta(days=1),
                                               message_text='Test message 2')
        self.client.force_authenticate(user=self.user)

    def test_list_mailings(self):
        response = self.client.get(reverse('mailing-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = MailingSerializer(Mailing.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_mailing(self):
        response = self.client.get(reverse('mailing-detail', args=[self.mailing1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['messages'], [])
        self.assertEqual(response.data['message_text'], self.mailing1.message_text)

    def test_patch_mailing(self):
        data = {'message_text': 'Updated Message'}
        response = self.client.patch(reverse('mailing-detail', args=[self.mailing1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message_text'], 'Updated Message')

    def test_put_mailing(self):
        data = {'start_time': timezone.now(), 'end_time': timezone.now() + timedelta(days=3),
                'message_text': 'New Message'}
        response = self.client.put(reverse('mailing-detail', args=[self.mailing1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message_text'], 'New Message')

    def test_delete_mailing(self):
        response = self.client.delete(reverse('mailing-detail', args=[self.mailing1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mailing.objects.filter(pk=self.mailing1.pk).exists())

    def test_create_mailing(self):
        data = {'start_time': timezone.now(), 'end_time': timezone.now() + timedelta(days=4),
                'message_text': 'New Test Message'}
        response = self.client.post(reverse('mailing-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_text'], 'New Test Message')
