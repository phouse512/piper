import datetime
import git
import json
import os

from django.http import HttpResponse


# basic heartbeater request
def index(request):
	repo = git.Repo(os.getcwd())
	master = repo.head.reference
	datetime_object = datetime.datetime.fromtimestamp(master.commit.committed_date)
	return_object = {
		'commitTime': str(datetime_object.utcnow()),
		'commitMessage': master.commit.message,
		'commitAuthor': master.commit.author.name
	}

	return HttpResponse(json.dumps(return_object), content_type="application/json")