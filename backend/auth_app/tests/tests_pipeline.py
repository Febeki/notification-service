from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from auth_app.pipeline import associate_by_email

User = get_user_model()


class AssociateByEmailTests(TestCase):
    @patch('auth_app.pipeline.RefreshToken')
    @patch('social_django.strategy.DjangoStrategy')
    def test_associate_by_email_with_existing_user(self, mock_strategy, mock_refresh_token):
        user = User.objects.create(email='test@example.com', username='testuser')

        mock_strategy.session_set = MagicMock()

        mock_refresh = MagicMock()
        mock_refresh.access_token = 'mock_access_token'
        mock_refresh.__str__.return_value = 'mock_refresh_token'
        mock_refresh_token.for_user.return_value = mock_refresh

        kwargs = {
            'details': {'email': user.email},
            'strategy': mock_strategy,
        }

        result = associate_by_email(**kwargs)

        self.assertEqual(result['user'], user)

        mock_strategy.session_set.assert_any_call('access_token', 'mock_access_token')
        mock_strategy.session_set.assert_any_call('refresh_token', 'mock_refresh_token')

    def test_associate_by_email_with_nonexistent_user(self):
        mock_strategy = MagicMock()
        kwargs = {
            'details': {'email': 'nonexistent@example.com'},
            'strategy': mock_strategy,
        }

        result = associate_by_email(**kwargs)

        self.assertIsNone(result.get('user'))
