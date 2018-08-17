import httplib

from django.http import JsonResponse
from swaggapi.api.builder.server.request import DjangoRequestView

from rotest.api.common.models import TestOperation
from rotest.api.common.responses import EmptyResponse
from rotest.api.test_control.middleware import session_middleware

# pylint: disable=unused-argument, no-self-use


class StopTest(DjangoRequestView):
    """End a test run.

    Args:
        test_id (number): the identifier of the test.
        token (str): token of the session.
    """
    URI = "tests/stop_test"
    DEFAULT_MODEL = TestOperation
    DEFAULT_RESPONSES = {
        httplib.NO_CONTENT: EmptyResponse,
    }
    TAGS = {
        "post": ["Tests"]
    }

    @session_middleware
    def post(self, request, sessions, *args, **kwargs):
        """End a test run.

        Args:
            request (Request): StopTest request.
        """
        session_token = request.model.token
        session_data = sessions[session_token]
        test_data = session_data.all_tests[request.model.test_id]
        test_data.end()
        test_data.save()

        return JsonResponse({}, status=httplib.NO_CONTENT)
