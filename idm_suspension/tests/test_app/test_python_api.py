"""
Tests for the internal Python API for idm_suspension
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now
from freezegun import freeze_time

from idm_suspension.models import Suspension
from idm_suspension.tests.test_app.models import Entitlement


class SuspensionPythonAPITestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='user')

    @freeze_time('2012-12-12T12:12:12+12:12')
    def test_suspend(self):
        e = Entitlement.objects.create()
        self.assertFalse(e.suspended)
        e.suspend(user=self.user, user_reason='Just for now')
        self.assertTrue(e.suspended)

        suspension = Suspension.objects.get()
        self.assertEqual('Just for now', suspension.user_reason)
        self.assertEqual(now(), suspension.start)