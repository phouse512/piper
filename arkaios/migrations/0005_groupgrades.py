# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0004_adminusers_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupGrades',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('group_hash', models.CharField(default=b'test', max_length=10)),
                ('option_value', models.CharField(max_length=30)),
            ],
        ),
    ]
