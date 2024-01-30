from django.test import TestCase
from unittest.mock import patch, MagicMock

from django.http import HttpRequest

from auth_app.middleware import JWTAuthMiddleware


class JWTAuthMiddlewareTest(TestCase):

    @patch('auth_app.middleware.validated_response')
    def test_process_request_with_tokens(self, mock_validated_response):
        middleware = JWTAuthMiddleware(get_response=MagicMock())

        request = HttpRequest()
        request.COOKIES['access_token'] = 'test_access_token'
        request.COOKIES['refresh_token'] = 'test_refresh_token'

        middleware.process_request(request)

        mock_validated_response.assert_called_once_with(request, middleware.get_response, 'test_access_token',
                                                        'test_refresh_token')

    def test_process_request_without_tokens(self):
        middleware = JWTAuthMiddleware(get_response=MagicMock())
        request = HttpRequest()
        result = middleware.process_request(request)

        self.assertIsNone(result)
