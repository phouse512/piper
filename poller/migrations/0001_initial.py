# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('open', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=1)),
                ('question', models.CharField(max_length=250)),
                ('correct_id', models.IntegerField(default=None)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('finish_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('score', models.IntegerField()),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=150)),
                ('pin', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=150)),
                ('join_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='scores',
            name='user',
            field=models.ForeignKey(to='poller.Users'),
        ),
        migrations.AddField(
            model_name='answers',
            name='poll',
            field=models.ForeignKey(related_name='answers', to='poller.Poll'),
        ),
    ]
