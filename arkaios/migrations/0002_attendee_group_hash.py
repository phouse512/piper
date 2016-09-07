# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='group_hash',
            field=models.CharField(default=b'test', max_length=10),
        ),
    ]
