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

        # new_poll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=1,
        #     question='Who will win Game 1 of the World Series?',
        #     correct_id=0,
        #     finish_time="2016-10-26 00:00:00+00"
        # )
        # #
        # cleveland_answer = Answers.objects.create(
        #     text="Cleveland Indians",
        #     poll=new_poll
        # )
        #
        # chicago_answer = Answers.objects.create(
        #     text="Chicago Cubs",
        #     poll=new_poll
        # )
        #
        # nyPoll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=1,
        #     question='New York Knicks versus Cleveland Cavaliers, NBA Opener',
        #     correct_id=0,
        #     finish_time="2016-10-25 23:30:00+00"
        # )
        #
        # cavs = Answers.objects.create(
        #     text="Cleveland Cavaliers",
        #     poll=nyPoll
        # )
        #
        # knicks = Answers.objects.create(
        #     text="New York Knicks",
        #     poll=nyPoll
        # )
        #
        # utahPoll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=1,
        #     question='Utah Jazz versus Portland Trailblazers, NBA Opener',
        #     correct_id=0,
        #     finish_time="2016-10-26 02:00:00+00"
        # )
        #
        # utah = Answers.objects.create(
        #     text="Utah Jazz",
        #     poll=utahPoll
        # )
        #
        # portland = Answers.objects.create(
        #     text="Portland Trailblazers",
        #     poll=utahPoll
        # )
        #
        # gsPoll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=1,
        #     question='San Antonio Spurs versus Golden State Warriors, NBA Opener',
        #     correct_id=0,
        #     finish_time="2016-10-26 02:30:00+00"
        # )
        #
        # spurs = Answers.objects.create(
        #     text="San Antonio Spurs",
        #     poll=gsPoll
        # )
        #
        # gs = Answers.objects.create(
        #     text="Golden State Warriors",
        #     poll=gsPoll
        # )


        # new_poll = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=2,
        #     question='total runs allowed by Cleveland pitching - Game 1',
        #     correct_id=0,
        #     finish_time="2016-10-26 00:00:00+00"
        # )
        # #
        # cleveland_answer = Answers.objects.create(
        #     text="0, 1, or 2",
        #     poll=new_poll
        # )
        #
        # chicago_answer = Answers.objects.create(
        #     text="3, 4, or 5",
        #     poll=new_poll
        # )
        #
        # third_answer = Answers.objects.create(
        #     text="more than 5",
        #     poll=new_poll
        # )
        #
        # cubs_pitching = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=2,
        #     question='total runs allowed by Chicago pitching - Game 1',
        #     correct_id=0,
        #     finish_time="2016-10-26 00:00:00+00"
        # )
        # #
        # little = Answers.objects.create(
        #     text="0, 1, or 2",
        #     poll=cubs_pitching
        # )
        #
        # middle = Answers.objects.create(
        #     text="3, 4, or 5",
        #     poll=cubs_pitching
        # )
        #
        # last = Answers.objects.create(
        #     text="more than 5",
        #     poll=cubs_pitching
        # )
        #
        # kyrie = Poll.objects.create(
        #     open=True,
        #     finished=False,
        #     weight=3,
        #     question='Kyrie Irving points total against NY Knicks',
        #     correct_id=0,
        #     finish_time="2016-10-25 23:30:00+00"
        # )
        # #
        # kyrie1 = Answers.objects.create(
        #     text="less than 15",
        #     poll=kyrie
        # )
        #
        # kyrie2 = Answers.objects.create(
        #     text="16 - 21",
        #     poll=kyrie
        # )
        #
        # kyrie3 = Answers.objects.create(
        #     text="more than 21",
        #     poll=kyrie
        # )
        #
        new_poll = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Chicago Cubs at Cleveland Indians - World Series Game 2',
            correct_id=0,
            finish_time="2016-10-27 23:00:00+00"
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

        cleveland_hitting = Poll.objects.create(
            open=True,
            finished=False,
            weight=2,
            question='total number of hits by Cleveland batters',
            correct_id=0,
            finish_time="2016-10-27 23:00:00+00"
        )
        #
        little = Answers.objects.create(
            text="less than 6",
            poll=cleveland_hitting
        )

        middle = Answers.objects.create(
            text="6, 7, or 8",
            poll=cleveland_hitting
        )

        last = Answers.objects.create(
            text="9 or more",
            poll=cleveland_hitting
        )

        chicago_hitting = Poll.objects.create(
            open=True,
            finished=False,
            weight=2,
            question='total number of hits by Chicago batters',
            correct_id=0,
            finish_time="2016-10-27 23:00:00+00"
        )
        #
        kyrie1 = Answers.objects.create(
            text="less than 6",
            poll=chicago_hitting
        )

        kyrie2 = Answers.objects.create(
            text="6, 7, or 8",
            poll=chicago_hitting
        )

        kyrie3 = Answers.objects.create(
            text="9 or more",
            poll=chicago_hitting
        )

        miami = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Miami Heat at Orlando Magic',
            correct_id=0,
            finish_time="2016-10-27 23:00:00+00"
        )
        #
        miami_heat = Answers.objects.create(
            text="Miami Heat",
            poll=miami
        )

        orland = Answers.objects.create(
            text="Orlando Magic",
            poll=miami
        )

        dallas = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Dallas Mavericks at Indiana Pacers',
            correct_id=0,
            finish_time="2016-10-27 23:00:00+00"
        )
        #
        dallas_mavs = Answers.objects.create(
            text="Dallas Mavericks",
            poll=dallas
        )

        orland = Answers.objects.create(
            text="Indiana Pacers",
            poll=dallas
        )

        brooklynceltics = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Brooklyn Nets at Boston Celtics',
            correct_id=0,
            finish_time="2016-10-27 23:30:00+00"
        )
        #
        brooklyn = Answers.objects.create(
            text="Brooklyn Nets",
            poll=brooklynceltics
        )

        celtics = Answers.objects.create(
            text="Boston Celtics",
            poll=brooklynceltics
        )

        detroitraptors = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Detroit Pistons at Toronto Raptors',
            correct_id=0,
            finish_time="2016-10-27 23:30:00+00"
        )
        #
        detroit = Answers.objects.create(
            text="Detroit Pistons",
            poll=detroitraptors
        )

        toronto = Answers.objects.create(
            text="Toronto Raptors",
            poll=detroitraptors
        )

        charlottebucks = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Charlotte Hornets at Milwaukee Bucks',
            correct_id=0,
            finish_time="2016-10-28 00:00:00+00"
        )
        #
        charlotte = Answers.objects.create(
            text="Charlotte Hornets",
            poll=charlottebucks
        )

        milwaukee = Answers.objects.create(
            text="Milwaukee Bucks",
            poll=charlottebucks
        )

        minnesotagrizzlies = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Minnesota Timberwolves at Memphis Grizzlies',
            correct_id=0,
            finish_time="2016-10-28 00:00:00+00"
        )
        #
        minnesota = Answers.objects.create(
            text="Minnesota Timberwolves",
            poll=minnesotagrizzlies
        )

        memphis = Answers.objects.create(
            text="Memphis Grizzlies",
            poll=minnesotagrizzlies
        )

        denver_pelicans = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Denver Nuggets at New Orleans Pelicans',
            correct_id=0,
            finish_time="2016-10-28 00:00:00+00"
        )

        denver = Answers.objects.create(
            text="Denver Nuggets",
            poll=denver_pelicans
        )

        neworleans = Answers.objects.create(
            text="New Orleans Pelicans",
            poll=denver_pelicans
        )

        oklahoma_sixers = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Oklahoma City Thunder at Philadelphia Sixers',
            correct_id=0,
            finish_time="2016-10-28 00:00:00+00"
        )

        okc = Answers.objects.create(
            text="Oklahoma City Thunder",
            poll=oklahoma_sixers
        )

        sixers = Answers.objects.create(
            text="Philadelphia Sixers",
            poll=oklahoma_sixers
        )

        sacramentosuns = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Sacramento Kings at Phoenix Suns',
            correct_id=0,
            finish_time="2016-10-28 02:00:00+00"
        )

        phoenix = Answers.objects.create(
            text="Phoenix Suns",
            poll=sacramentosuns
        )

        kings = Answers.objects.create(
            text="Sacramento Kings",
            poll=sacramentosuns
        )

        houston_lakers = Poll.objects.create(
            open=True,
            finished=False,
            weight=1,
            question='Houston Rockets at Los Angeles Lakers',
            correct_id=0,
            finish_time="2016-10-28 02:00:00+00"
        )

        houston = Answers.objects.create(
            text="Houston Rockets",
            poll=houston_lakers
        )

        lakers = Answers.objects.create(
            text="Los Angeles Lakers",
            poll=houston_lakers
        )