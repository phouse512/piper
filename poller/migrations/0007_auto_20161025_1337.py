# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0006_auto_20161025_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scores',
            name='score',
        ),
        migrations.RemoveField(
            model_name='votes',
            name='points',
        ),
        migrations.AddField(
            model_name='scores',
            name='points',
            field=models.DecimalField(default=0, max_digits=15, decimal_places=3),
        ),
        migrations.AddField(
            model_name='scores',
            name='vote',
            field=models.ForeignKey(default=1, to='poller.Votes'),
            preserve_default=False,
        ),
    ]
