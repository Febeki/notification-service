from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='test', password='password1234', first_name='Test')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), 'test')

    def test_create_super_user(self):
        user = User.objects.create_superuser(username='test', password='password1234')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
