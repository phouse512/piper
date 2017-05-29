import datetime
import json
import requests
import time

from tallyclient import TallyClient

# os.environ['DJANGO_SETTINGS_MODULE'] = sys.path + 'piper.settings'

# from django.db.models.loading import get_models
# loaded_models = get_models()
#
from github.models import CommitLog
from github.models import FileModificationLog
from github.models import GithubIntegration
from ingester.task import Job

GITHUB_URL = "https://api.github.com"
GET_EVENTS_URL = "/users/%s/events"
GET_USER_REPOS_URL = "/user/repos?page=%s&per_page=100"
GET_ALL_USER_REPOS_URL = "/users/%s/repos?page=%s&per_page=100"
GET_REPO_COMMITS_URL = "/repos/%s/commits?per_page=100"
GET_COMMIT_FROM_SHA = "/repos/%s/commits/%s"

client = TallyClient('localhost', 8173)


class GithubCodeActivityJob(Job):

    def __init__(self, time, day_delta):
        self.time = time
        self.day_delta = day_delta

    def run(self):
        return self.github_commit_job()

    def github_commit_job(self):
        start_time = time.time()

        github_accounts = GithubIntegration.objects.all()
        instances = 0
        commits = 0

        for account in github_accounts:
            print account
            account_dict = {
                'id': account.id,
                'access_token': account.oauth_token,
                'username': account.github_username
            }
            try:
                commits += self.get_single_history(account_dict)
                instances += 1
            except Exception as e:
                print e

        client.count("piper.github_job")
        end_time = time.time()
        client.gauge("piper.github_job.responseTime", int((end_time-start_time) * 1000))
        return {
            'commits_saved': commits,
            'accounts_checked': instances,
            'account_success_ratio': float(instances/len(github_accounts))
        }

    def get_single_history(self, user):
        # print user
        user_repos = self.get_all_repos(user)

        for test in user_repos:
            print test

        print len(user_repos)
        commits = []
        for repo in user_repos:
            temp_commits = self.get_commits_for_repo_and_user(user, repo['full_name'], self.day_delta)
            print repo['full_name']
            commits.extend(temp_commits)

        # print json.dumps(commits)
        stats = []
        for commit in commits:
            try:
                # print commit['sha']
                test_commit = self.get_commit_from_sha(user, commit['full_repo'], commit['sha'])
                test_commit['_phil_test_repo_name'] = commit['full_repo']
                stats.append(test_commit)
            except Exception as e:
                yoza = 1
                print "found exception %s, skipping commit %s" % (str(e), commit)

        print "number of commits: %d" % len(stats)
        self.save_single_user_data(stats)

        return len(stats)

        # print len(stats)

    def get_all_repos(self, user, page=1):

        request_url = GITHUB_URL + GET_USER_REPOS_URL % page

        r = requests.get(request_url, auth=(user['username'], user['access_token']),
                         params={'affiliation': 'owner,collaborator,organization_member'})
        # TODO get all repos from organizations:
        # https://developer.github.com/v3/orgs/#list-your-organizations
        user_repos = []
        for repo in r.json():
            temp_repo = {
                'id': repo['id'],
                'full_name': repo['full_name']
            }
            user_repos.append(temp_repo)

        if len(user_repos) >= 100:
            page += 1
            return user_repos + self.get_all_repos(user, page)

        return user_repos
        # print json.dumps(user_repos)
        # print json.dumps(r.json())

    def get_commits_for_repo_and_user(self, user, repo_full_name, time_delta=1):
        current_time = datetime.datetime.now()
        since = current_time - datetime.timedelta(days=time_delta)
        params = {
            'author': user['username'],
            'until': current_time.isoformat(),
            'since': since.isoformat()
        }

        request_url = GITHUB_URL + GET_REPO_COMMITS_URL % repo_full_name
        r = requests.get(request_url, auth=(user['username'], user['access_token']), params=params)

        # attach repo to each commit if there is a list of commits
        result = r.json()
        if isinstance(result, list):
            for i in result:
                i['full_repo'] = repo_full_name
        return result

    def get_commit_from_sha(self, user, repo_full_name, sha):
        request_url = GITHUB_URL + GET_COMMIT_FROM_SHA % (repo_full_name, sha)
        r = requests.get(request_url, auth=(user['username'], user['access_token']))

        return r.json()

    def save_single_user_data(self, all_commits):
        if len(all_commits) < 1:
            return

        for commit in all_commits:
            try:
                self.save_single_commit(commit)
            except ValueError as e:
                # logging should go here for commits changing json
                print "yo json issues"
                print e

        return all_commits

    def save_single_commit(self, commit):
        sha = commit['sha']

        existing_commit = CommitLog.objects.filter(sha=sha).first()
        if existing_commit:
            old_file_logs = FileModificationLog.objects.filter(commit_id=existing_commit.id).delete()
            existing_commit.delete()

        new_commit = CommitLog.objects.create(
            github_id=commit['author']['id'],
            time=commit['commit']['author']['date'],
            sha=commit['sha'],
            additions=commit['stats']['additions'],
            deletions=commit['stats']['deletions'],
            repo_name=commit['_phil_test_repo_name']
        )

        for file in commit['files']:
            new_file = FileModificationLog(
                commit=new_commit,
                status=file['status'],
                additions=file['additions'],
                deletions=file['deletions'],
                file_name=file['filename'],
                file_extension=file['filename'].split(".")[-1]
            ).save()
