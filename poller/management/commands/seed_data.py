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

        poll = Poll.objects.filter(id=4).first()

        print poll.votes.all()

        # new_poll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=1,
        #     question='Who will win Game 1 of the World Series?',
        #     correct_id=0,
        #     finish_time=datetime.datetime.now() + datetime.timedelta(days=3)
        # )
        #
        # cleveland_answer = Answers.objects.create(
        #     text="Cleveland Indians",
        #     poll=new_poll
        # )
        #
        # chicago_answer = Answers.objects.create(
        #     text="Chicago Cubs",
        #     poll=new_poll
        # )


