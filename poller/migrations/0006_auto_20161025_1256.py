# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0005_users_points_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='points_total',
            field=models.DecimalField(default=0, max_digits=15, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='votes',
            name='points',
            field=models.DecimalField(default=0, max_digits=15, decimal_places=3),
        ),
    ]
