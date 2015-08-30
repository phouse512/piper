# from django.shortcuts import render

import json
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from users.models import User
from users.forms import SignupForm
from users.forms import LoginForm


def index(request):
    users = User.objects.get()
    return HttpResponse(serializers.serialize('json', [users]), content_type="application/json")


@require_POST
@csrf_exempt
def signup(request):

    # this is a form submission
    form = SignupForm(request.POST)

    if not form.is_valid():
        # this means we were sent a bad request - let the front end know
        return HttpResponse("failure")

    if User.objects.filter(username=form.cleaned_data['username']).exists():
        return HttpResponse("user already exists sucka")

    new_user = User(
        username=form.cleaned_data['username'],
        email=form.cleaned_data['email'],
        phone=form.cleaned_data['phone'],
        password=make_password(form.cleaned_data['password'], 'saltysalt', 'bcrypt'),
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        access_token=uuid.uuid4(),
    ).save()

    object = {
        'access_token': new_user.access_token
    }

    return HttpResponse(json.dumps(object), content_type="application/json")


@require_POST
@csrf_exempt
def login(request):

    form = LoginForm(request.POST)

    if not form.is_valid():
        # this means we were sent a bad request - let someone know :o
        return HttpResponse("failure")

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
        return HttpResponse("user had the right credentials")
    else:
        return HttpResponse("wrong credentials sucker")
