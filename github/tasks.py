import datetime
import json
import requests
import os
import sys

# os.environ['DJANGO_SETTINGS_MODULE'] = sys.path + 'piper.settings'

# from django.db.models.loading import get_models
# loaded_models = get_models()
#
from github.models import GithubIntegration
from ingester.task import Job

GITHUB_URL = "https://api.github.com"
GET_EVENTS_URL = "/users/%s/events"
GET_USER_REPOS_URL = "/users/%s/repos"
GET_REPO_COMMITS_URL = "/repos/%s/commits"
GET_COMMIT_FROM_SHA = "/repos/%s/commits/%s"

### COMMENT THIS OUT
# user = {
#     'id': 1,
#     'access_token': '',
#     'username': 'phouse512',
# }


class GithubCodeActivityJob(Job):

    def __init__(self, time):
        self.time = time

    def run(self):
        self.github_commit_job()

    @staticmethod
    def github_commit_job(self):
        current_time = datetime.datetime.now()

        # github_accounts = GithubIntegration.objects.all()

        # for account in github_accounts:
        #     print account
            # store commits


    def get_single_history(self, user):
        print user
        user_repos = self.get_all_repos(user)

        print len(user_repos)
        commits = []
        for repo in user_repos:
            temp_commits = self.get_commits_for_repo_and_user(user, repo['full_name'])
            print repo['full_name']
            print temp_commits
            commits.extend(temp_commits)

        print commits

        # print [commit['sha'] for commit in commits]


    def get_all_repos(self, user):

        request_url = GITHUB_URL + GET_USER_REPOS_URL % user['username']

        r = requests.get(request_url, auth=(user['username'], user['access_token']), params={'type': 'all' })

        user_repos = []
        for repo in r.json():
            temp_repo = {
                'id': repo['id'],
                'full_name': repo['full_name']
            }
            user_repos.append(temp_repo)

        return user_repos
        # print json.dumps(user_repos)
        # print json.dumps(r.json())


    def get_commits_for_repo_and_user(self, user, repo_full_name, time_delta=2):
        current_time = datetime.datetime.now()
        since = current_time - datetime.timedelta(days=time_delta)
        params = {
            'author': user['username'],
            'until': current_time.isoformat(),
            'since': since.isoformat()
        }

        request_url = GITHUB_URL + GET_REPO_COMMITS_URL % repo_full_name
        r = requests.get(request_url, auth=(user['username'], user['access_token']), params=params)

        return r.json()

    def get_commit_from_sha(user, repo_full_name, sha):
        request_url = GITHUB_URL + GET_COMMIT_FROM_SHA % (repo_full_name, sha)
        r = requests.get(request_url, auth=(user['username'], user['access_token']))

        print json.dumps(r.json())
