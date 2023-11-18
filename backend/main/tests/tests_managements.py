from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class ManagementTest(TestCase):
    def test_wait_for_db(self):
        out = StringIO()
        call_command('wait_for_db', stdout=out)
        self.assertIn('Database available!', out.getvalue())

    def test_create_superuser(self):
        out = StringIO()
        call_command('create_superuser', stdout=out)
        ans = out.getvalue()
        self.assertTrue(('Superuser created successfully' in ans) or ('Superuser already exists' in ans))
