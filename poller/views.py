import base64

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from functools import wraps

from poller.models import Poll, Answers, Votes
from poller.models import Users

# Create your views here.


def authenticate(username, pin):
    user = Users.objects.filter(username=username, pin=pin)
    if not user:
        return None
    return user


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    username, password = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username, password)
                    if user:
                        kwargs['user'] = user.first()
                        return f(*args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
        response.content = 'UNAUTHORIZED, get the right creds plz'
        return response

    return decorated


def home(request):

    active_polls = Poll.objects.filter(open=True, finished=False).all()

    return render(request, 'home.html', {'polls': active_polls})


@requires_auth
def view_poll(request, poll_id, **kwargs):
    poll = get_object_or_404(Poll, id=poll_id)

    return render(request, 'poll.html', {'poll': poll})


def signup(request):
    return render(request, 'signup.html')


@requires_auth
def save_vote(request, poll_id, answer_id, **kwargs):
    poll = get_object_or_404(Poll, id=poll_id)
    answer = get_object_or_404(Answers, id=answer_id)
    user = kwargs.get('user')
    print user

    if not poll.open or poll.finished:
        print "hm"
        return HttpResponseRedirect(reverse('view_poll', kwargs={ 'poll_id': poll_id}))

    new_vote = Votes.objects.create(
        poll=poll,
        user=user
    )
    print "HAR"
    return redirect('poller.views.view_poll', poll_id=poll_id)
