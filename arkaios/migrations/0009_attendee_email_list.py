# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0008_event_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='email_list',
            field=models.BooleanField(default=True),
        ),
    ]
