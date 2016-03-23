# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingester', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngesterJob',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=300)),
                ('last_run', models.DateTimeField()),
                ('job_class', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ingester_job',
            },
        ),
    ]
