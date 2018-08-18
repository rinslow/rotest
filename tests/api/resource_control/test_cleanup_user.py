"""Basic unittests for the server resource control operations."""
import httplib
from functools import partial

from django.test import Client, TransactionTestCase

from tests.api.utils import request
from rotest.management.models import DemoComplexResourceData


class TestCleanupUser(TransactionTestCase):
    """Assert operations of cleanup user request."""
    fixtures = ['resource_ut.json']

    def setUp(self):
        """Setup test environment."""
        self.client = Client()
        self.requester = partial(request, client=self.client,
                                 path="resources/cleanup_user")

    def test_no_resources_locked(self):
        """Assert response - cleanup when user didn't lock anything."""
        response, content = self.requester()
        self.assertEqual(response.status_code, httplib.OK)
        self.assertEqual(content.details,
                         "User localhost didn't lock any resource")

    def test_release_owner_complex_resource(self):
        """Assert response - cleanup of complex resource."""
        resources = DemoComplexResourceData.objects.filter(
            name='complex_resource1')

        resource, = resources
        sub_resource = resource.demo1

        resource.owner = "localhost"
        sub_resource.owner = "localhost"
        resource.save()
        sub_resource.save()
        response, _ = self.requester()
        self.assertEqual(response.status_code, httplib.OK)

        resources = DemoComplexResourceData.objects.filter(
            name='complex_resource1')

        resource, = resources
        sub_resource = resource.demo1

        self.assertEqual(resource.owner, "")
        self.assertEqual(sub_resource.owner, "")
