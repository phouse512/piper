# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0002_attendee_group_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('group_hash', models.CharField(default=b'test', max_length=10)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('on', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EventAttendance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('first_time', models.IntegerField(default=0)),
                ('attendee', models.ForeignKey(to='arkaios.Attendee')),
                ('event', models.ForeignKey(to='arkaios.Event')),
            ],
        ),
    ]
