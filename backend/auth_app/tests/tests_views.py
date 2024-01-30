from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CheckAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.url = reverse('check-auth')

    def test_check_auth_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_auth_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"isAuthenticated": True})


class CustomTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.url = reverse('token_obtain_pair')

    def test_token_obtain_pair(self):
        data = {
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)


class GoogleCompleteViewTests(APITestCase):

    @patch.dict('os.environ', {'OAUTH_REDIRECT_URL': 'http://testserver/'})
    def test_google_complete(self):
        url = reverse('google_complete')
        session = self.client.session
        session['access_token'] = 'test_access_token'
        session['refresh_token'] = 'test_refresh_token'
        session.save()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(response.has_header('Location'))
        self.assertIn('http://testserver/', response['Location'])

        self.assertTrue(response.cookies.get('access_token'))
        self.assertTrue(response.cookies.get('refresh_token'))
