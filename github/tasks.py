import requests
import json

GITHUB_URL = "https://api.github.com"
GET_EVENTS_URL = "/users/%s/events"

def get_single_history(user, access_token, username):

    request_url = GITHUB_URL + GET_EVENTS_URL % username

    r = requests.get(request_url, auth=(username, access_token))

    print json.dumps(r.json())


get_single_history('test', '7f1eed3cc6c632e736c3c7f7948d86016412cca3', 'phouse512')
