import httplib2
import sys
from oauth2client import client

"""
the hackiest code of all time to help get auth tokens
TODO: clean up one day
"""

flow = client.flow_from_clientsecrets('client_secrets.json', scope=['https://www.googleapis.com/auth/gmail.readonly', 'https://mail.google.com/', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/script.external_request'], redirect_uri='http://www.phizzle.space')
flow.params['access_type'] = 'offline'
flow.params['include_granted_scopes'] = 'true'

auth_uri = flow.step1_get_authorize_url()
print(auth_uri)

if len(sys.argv) < 2:
    print("step 1, quiting now")
    sys.exit()

print("starting step 2")
code = sys.argv[1]

credentials = flow.step2_exchange(code)
print(credentials)
print(credentials.to_json())
http_auth = credentials.authorize(httplib2.Http())
print(http_auth)

