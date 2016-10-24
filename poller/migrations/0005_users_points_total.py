# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0004_auto_20161024_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='points_total',
            field=models.IntegerField(default=0),
        ),
    ]
