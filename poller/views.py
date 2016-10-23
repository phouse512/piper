from django.shortcuts import render

from poller.models import Poll, Answers

# Create your views here.


def home(request):

    active_polls = Poll.objects.filter(open=True, finished=False).all()

    return render(request, 'home.html', {'polls': active_polls})
