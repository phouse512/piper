import base64

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from functools import wraps

from poller.models import Poll, Answers, Votes
from poller.models import Users
from poller.forms import SignupForm

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


def attach_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print "hm"
        request = args[0]

        if 'HTTP_AUTHORIZATION' in request.META:
            print "http"
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                print "len"
                if auth[0].lower() == 'basic':
                    print "i'm basic"
                    username, password = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username, password)
                    print user
                    if user:
                        kwargs['login_user'] = user.first()

        return f(*args, **kwargs)
    return decorated


@requires_auth
def home(request, **kwargs):

    active_polls = Poll.objects.filter(open=True, finished=False).all()
    login_user = kwargs.get('user', None)
    leaderboard_by_points = Users.objects.order_by('-points_total').all()

    leaderboard_by_votes = Users.objects.annotate(num_votes=Count('votes')).order_by('-num_votes')
    print leaderboard_by_votes

    return render(request, 'home.html', {'polls': active_polls, 'user': login_user,
                                         'points_leaderboard': leaderboard_by_points,
                                         'votes_leaderboard': leaderboard_by_votes})


@requires_auth
def view_poll(request, poll_id, **kwargs):
    poll = get_object_or_404(Poll, id=poll_id)

    login_user = kwargs.get('user')

    return render(request, 'poll.html', {'poll': poll, 'user': login_user})



@requires_auth
def profile(request, **kwargs):
    login_user = kwargs.get('user')
    votes = Votes.objects.filter(user=login_user).select_related('answer').all()

    return render(request, 'profile.html', {'user': login_user, 'votes': votes})


def signup(request):
    return render(request, 'signup.html')


def logout(request):
    return render(request, 'logout.html')


def create_user(request):
    form = SignupForm(request.POST)
    if form.is_valid():

        existing_user = Users.objects.filter(username=form.cleaned_data['username']).first()
        if existing_user:
            messages.add_message(request, messages.ERROR, "A user with that username already exists.")
            return redirect('poller.views.signup')

        new_user = Users.objects.create(
            username=form.cleaned_data['username'],
            pin=form.cleaned_data['pinInput'],
            email=form.cleaned_data['emailInput']
        )

        # create user

        messages.add_message(request, messages.INFO, "You've successfully signed up!")
        return redirect('poller.views.home')

    print form.errors
    messages.add_message(request, messages.WARNING, "invalid form, please fill in all fields and make pw less than 11 chars")
    return redirect('poller.views.signup')

@requires_auth
def save_vote(request, poll_id, answer_id, **kwargs):
    poll = get_object_or_404(Poll, id=poll_id)
    answer = get_object_or_404(Answers, id=answer_id)
    user = kwargs.get('user')
    print user

    if not poll.open or poll.finished:
        messages.add_message(request, messages.INFO, 'Sorry, this poll is closed.')
        return HttpResponseRedirect(reverse('view_poll', kwargs={ 'poll_id': poll_id}))

    existing_vote = Votes.objects.filter(user=user, poll=poll).first()
    if existing_vote:
        messages.add_message(request, messages.INFO, 'Updated your vote.')
        existing_vote.answer = answer
        existing_vote.save()
        return redirect('poller.views.view_poll', poll_id)

    new_vote = Votes.objects.create(
        poll=poll,
        user=user,
        answer=answer
    )

    messages.add_message(request, messages.INFO, 'Successfully saved your vote.')
    return redirect('poller.views.view_poll', poll_id=poll_id)
