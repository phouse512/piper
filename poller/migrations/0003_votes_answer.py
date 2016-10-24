# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0002_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='votes',
            name='answer',
            field=models.ForeignKey(related_name='votes', default=1, to='poller.Answers'),
            preserve_default=False,
        ),
    ]
