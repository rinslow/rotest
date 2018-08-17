"""Abstract TestCase for all resources related tests."""
# pylint: disable=too-many-public-methods,invalid-name
import time

import subprocess
from django.test.testcases import TransactionTestCase

from rotest.core.result.result import Result
from rotest.core.result.handlers.db_handler import DBHandler


class BaseResourceManagementTest(TransactionTestCase):
    """Abstract TestCase for resources related tests.

    Allow multiple access to the DB from different threads by deriving from
    TransactionTestCase. Every test that use resource manager directly or
    indirectly (using Case) should run the server before it starts. Deriving
    from this class will start the resource manager server in an independent
    thread on the setUp of each test and stop in on the tearDown.
    """
    SERVER_STARTUP_TIME = 2

    def setUp(self):
        """Start ResourceManagerServer in an independent thread."""
        self.server = subprocess.Popen("python manage.py runserver",
                                       shell=True)

        time.sleep(self.SERVER_STARTUP_TIME)

    def tearDown(self):
        """Stop resource manager server."""
        self.server.kill()

    @staticmethod
    def create_result(main_test):
        """Create a result object for the test and starts it.

        Args:
            main_test(TestSuite / TestCase): the test to be ran.

        Returns:
            Result. a new initiated result object.
        """
        result = Result(outputs=[DBHandler.NAME], main_test=main_test)
        result.startTestRun()
        return result
