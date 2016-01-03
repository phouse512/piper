import datetime
import json
import requests

from github.models import GithubIntegration

GITHUB_URL = "https://api.github.com"
GET_EVENTS_URL = "/users/%s/events"
GET_USER_REPOS_URL = "/users/%s/repos"
GET_REPO_COMMITS_URL = "/repos/%s/commits"
GET_COMMIT_FROM_SHA = "/repos/%s/commits/%s"

### COMMENT THIS OUT
user = {
    'id': 1,
    'access_token': '',
    'username': 'phouse512',
}


def github_commit_job():
    current_time = datetime.datetime.now()

    github_accounts = GithubIntegration.objects.all()

    for account in github_accounts:
        print account
        # store commits


def get_single_history(user, access_token, username):

    request_url = GITHUB_URL + GET_EVENTS_URL % username

    r = requests.get(request_url, auth=(username, access_token))

    print json.dumps(r.json())


def get_all_repos(user):

    request_url = GITHUB_URL + GET_USER_REPOS_URL % user['username']

    r = requests.get(request_url, auth=(user['username'], user['access_token']), params={'type': 'all' })

    user_repos = []
    for repo in r.json():
        temp_repo = {
            'id': repo['id'],
            'full_name': repo['full_name']
        }
        user_repos.append(temp_repo)

    print json.dumps(user_repos)
    # print json.dumps(r.json())


def get_commits_for_repo_and_user(user, repo_full_name, user_commits, time_delta=1):
    current_time = datetime.datetime.now()
    since = current_time - datetime.timedelta(days=time_delta)
    params = {
        'author': user['username'],
        'until': current_time.isoformat(),
        'since': since.isoformat()
    }

    request_url = GITHUB_URL + GET_REPO_COMMITS_URL % repo_full_name
    r = requests.get(request_url, auth=(user['username'], user['access_token']), params=params)

    print json.dumps(r.json())

def get_commit_from_sha(user, repo_full_name, sha):
    request_url = GITHUB_URL + GET_COMMIT_FROM_SHA % (repo_full_name, sha)
    r = requests.get(request_url, auth=(user['username'], user['access_token']))

    print json.dumps(r.json())

# get_all_repos(user)
# get_commits_for_repo_and_user(user, 'phouse512/piper', [], 2)
get_commit_from_sha(user, 'phouse512', 'sha')
