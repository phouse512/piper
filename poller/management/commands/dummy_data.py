from django.core.management.base import BaseCommand
from poller.models import Poll, Answers, Users


class Command(BaseCommand):
    help = 'Seeds the database with some dummy data, don\'t run live'

    def handle(self, *args, **options):
        # all the dummy data
        print "hi"

