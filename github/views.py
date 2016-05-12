from datetime import datetime
import json
import requests

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_POST

from github.models import GithubIntegration
from github.tasks import GithubCodeActivityJob
from integrations.models import Integrations
from users.models import User

GET_GITHUB_USER = "https://api.github.com/user"

@require_POST
@csrf_exempt
def connect(request):
    access_token = request.POST['accessToken']
    piper_id = int(request.POST['piperId'])

    user = get_object_or_404(User, pk=piper_id)
    # in the future we might need to check for expired time - for now we can't

    payload = { 'access_token': access_token }
    response = requests.get(GET_GITHUB_USER, params=payload)

    if response.status_code != 200:
        failure = {
            'status': response.status_code,
            'responseBody': response.json(),
            'message': 'github get user call is failing'
        }
        return HttpResponse(json.dumps(failure), content_type="application/json")

    github_integration = GithubIntegration(
        user=user,
        github_id=response.json()['id'],
        github_username=response.json()['login'],
        oauth_token=access_token,
        oauth_is_valid=True
    ).save()

    integration = Integrations(
        user=user,
        network_id=github_integration.id,
        type="github"
    ).save()

    response = {
        'integrationId': integration.id,
        'githubIntegrationId': github_integration.id,
        'githubName': github_integration.github_username
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def test(request):
    return "yo"


def github_job(request):
    job = GithubCodeActivityJob(datetime.now())
    success = job.run()

    response_dict = {
        'success_ratio': success
    }

    return HttpResponse(json.dumps(response_dict), content_type="application/json")
