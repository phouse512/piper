# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0003_event_eventattendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUsers',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=150)),
                ('pw_hash', models.CharField(max_length=512)),
                ('last_login', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('group_hash', models.CharField(default=b'test', max_length=10)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
    ]
