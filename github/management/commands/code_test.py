import datetime

from django.core.management.base import BaseCommand, CommandError
from github.models import GithubIntegration
from github.tasks import GithubCodeActivityJob
from piper import settings


class Command(BaseCommand):
    help = 'Tests the github scraping command'

    def handle(self, *args, **options):
        # print "YOOOO"

        user = {
            'id': 1,
            'access_token': settings.GITHUB_TEST_KEY,
            'username': 'phouse512',
        }

        github_job = GithubCodeActivityJob(datetime.datetime.now(), 3)
        # github_job.get_commits_for_repo_and_user(user, 'phouse512/piper', 10)

        github_job.get_single_history(user)

        # self.stdout.write("DONE TESTING!")
