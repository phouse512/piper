# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0006_groupadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventattendance',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
