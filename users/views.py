# from django.shortcuts import render

import json

from django.http import HttpResponse
from users.models import User

def index(request):
    users = User.objects.get().all()
    return HttpResponse(json.dumps(users), content_type="application/json")