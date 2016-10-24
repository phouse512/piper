import datetime

from django.core.management.base import BaseCommand
from poller.models import Poll, Answers, Users


class Command(BaseCommand):
    help = 'Seeds the database with some questions'

    def handle(self, *args, **options):

        # new_user = Users.objects.create(
        #     username='phouse512',
        #     pin='60201',
        #     email='philiphouse2015@u.northwestern.edu'
        # )

        # poll = Poll.objects.filter(id=4).first()
        #
        # print poll.votes.all()

        new_poll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Who will win Game 1 of the World Series?',
            correct_id=0,
            finish_time="2016-10-26 00:00:00+00"
        )
        #
        cleveland_answer = Answers.objects.create(
            text="Cleveland Indians",
            poll=new_poll
        )

        chicago_answer = Answers.objects.create(
            text="Chicago Cubs",
            poll=new_poll
        )

        nyPoll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='New York Knicks versus Cleveland Cavaliers, NBA Opener',
            correct_id=0,
            finish_time="2016-10-25 23:30:00+00"
        )

        cavs = Answers.objects.create(
            text="Cleveland Cavaliers",
            poll=nyPoll
        )

        knicks = Answers.objects.create(
            text="New York Knicks",
            poll=nyPoll
        )

        utahPoll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Utah Jazz versus Portland Trailblazers, NBA Opener',
            correct_id=0,
            finish_time="2016-10-26 02:00:00+00"
        )

        utah = Answers.objects.create(
            text="Utah Jazz",
            poll=utahPoll
        )

        portland = Answers.objects.create(
            text="Portland Trailblazers",
            poll=utahPoll
        )

        gsPoll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='San Antonio Spurs versus Golden State Warriors, NBA Opener',
            correct_id=0,
            finish_time="2016-10-26 02:30:00+00"
        )

        spurs = Answers.objects.create(
            text="San Antonio Spurs",
            poll=gsPoll
        )

        gs = Answers.objects.create(
            text="Golden State Warriors",
            poll=gsPoll
        )