import datetime

from django.core.management.base import BaseCommand
from poller.models import Poll, Answers


class Command(BaseCommand):
    help = 'Seeds the database with some questions'

    def handle(self, *args, **options):

        new_poll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Who will win Game 1 of the World Series?',
            correct_id=0,
            finish_time=datetime.datetime.now() + datetime.timedelta(days=3)
        )

        cleveland_answer = Answers.objects.create(
            text="Cleveland Indians",
            poll=new_poll
        )

        chicago_answer = Answers.objects.create(
            text="Chicago Cubs",
            poll=new_poll
        )


