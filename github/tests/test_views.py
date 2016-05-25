import json

from django.test import SimpleTestCase
from django.test.client import RequestFactory
from mock import MagicMock
from mock import patch

from github.views import commit_tail


class GithubTailTests(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()

    @patch('github.views.get_object_or_404')
    @patch('github.views.CommitLog')
    def test_basic_github_tail(self, commit_log_patch, get_object_patch):
        account = MagicMock()
        request = self.rf.get('/github/tail/phouse512/')
        username = "phouse512"

        get_object_patch.return_value = account
        commit_log_patch.objects.filter.return_value = []

        response = commit_tail(request, username)

        self.assertEqual(200, response.status_code)
        self.assertEqual([], json.loads(response.content))

