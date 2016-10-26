from django.core.management.base import BaseCommand
from poller.models import Poll, Answers, Users
from poller.scoring import score_poll


class Command(BaseCommand):
    help = 'Seeds the database with some dummy data, don\'t run live'

    def handle(self, *args, **options):
        # all the dummy data
        print "hi"

        poll_id = int(args[0])
        answer_id = int(args[1])
        save = bool(args[2])

        print "poll id: " + str(poll_id)
        print "answer id: " + str(answer_id)
        print "save: " + str(save)

        print score_poll(poll_id, answer_id, save)
