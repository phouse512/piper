# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('poll', models.ForeignKey(related_name='votes', to='poller.Poll')),
                ('user', models.ForeignKey(related_name='votes', to='poller.Users')),
            ],
        ),
    ]
