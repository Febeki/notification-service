from unittest.mock import MagicMock, patch

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from rest_framework_simplejwt.exceptions import TokenError

from auth_app.services import response_with_tokens_in_cookies, response_without_tokens, validated_response


class TestValidatedResponse(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    @patch('auth_app.services.AccessToken')
    def test_access_token_valid(self, mock_access_token):
        mock_get_response = MagicMock()

        validated_response(self.request, mock_get_response, 'valid_access_token', 'valid_refresh_token')

        mock_access_token.assert_called_with('valid_access_token')
        mock_get_response.assert_not_called()
        self.assertEqual(self.request.META['HTTP_AUTHORIZATION'], 'Bearer valid_access_token')

    @patch('auth_app.services.AccessToken')
    @patch('auth_app.services.RefreshToken')
    @patch('auth_app.services.response_with_tokens_in_cookies')
    def test_access_token_invalid_refresh_token_valid(self, mock_response_with_tokens, mock_refresh_token,
                                                      mock_access_token):
        mock_get_response = MagicMock()
        mock_access_token.side_effect = TokenError
        mock_valid_refresh_token = MagicMock()
        mock_refresh_token.return_value = mock_valid_refresh_token
        mock_valid_refresh_token.access_token = 'new_access_token'

        validated_response(self.request, mock_get_response, 'invalid_access_token', 'valid_refresh_token')

        mock_access_token.assert_called_with('invalid_access_token')
        mock_refresh_token.assert_called_with('valid_refresh_token')
        mock_response_with_tokens.assert_called_once_with(mock_get_response.return_value, 'new_access_token',
                                                          'valid_refresh_token')

    @patch('auth_app.services.AccessToken')
    @patch('auth_app.services.RefreshToken')
    @patch('auth_app.services.response_without_tokens')
    def test_both_tokens_invalid(self, mock_response_without_tokens, mock_refresh_token, mock_access_token):
        mock_get_response = MagicMock()
        mock_access_token.side_effect = TokenError
        mock_refresh_token.side_effect = TokenError

        validated_response(self.request, mock_get_response, 'invalid_access_token', 'invalid_refresh_token')

        mock_access_token.assert_called_with('invalid_access_token')
        mock_refresh_token.assert_called_with('invalid_refresh_token')
        mock_response_without_tokens.assert_called_once_with(mock_get_response.return_value)


class TestResponseWithTokensInCookies(TestCase):

    def test_response_with_tokens(self):
        response = HttpResponse()
        modified_response = response_with_tokens_in_cookies(response, 'access_token_value', 'refresh_token_value')

        self.assertIn('access_token', modified_response.cookies)
        self.assertIn('refresh_token', modified_response.cookies)
        self.assertTrue(modified_response.cookies['access_token']['httponly'])
        self.assertEqual(modified_response.cookies['access_token'].value, 'access_token_value')


class TestResponseWithoutTokens(TestCase):

    def test_response_without_tokens(self):
        response = HttpResponse()
        response.set_cookie('access_token', 'value')
        response.set_cookie('refresh_token', 'value')

        modified_response = response_without_tokens(response)

        self.assertEqual(modified_response.cookies['access_token'].value, '')
        self.assertEqual(modified_response.cookies['refresh_token'].value, '')

        self.assertTrue('Thu, 01 Jan 1970' in modified_response.cookies['access_token']['expires'])
        self.assertTrue('Thu, 01 Jan 1970' in modified_response.cookies['refresh_token']['expires'])
