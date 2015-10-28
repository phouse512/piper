# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngesterTask',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=6)),
                ('json_selector', models.CharField(max_length=100)),
                ('frequency', models.CharField(max_length=30)),
                ('integration_type', models.CharField(max_length=30)),
                ('periodic_task', models.ForeignKey(to='djcelery.PeriodicTask')),
            ],
            options={
                'db_table': 'ingester_task',
            },
        ),
        migrations.CreateModel(
            name='IngesterTaskHeaders',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('task', models.ForeignKey(to='ingester.IngesterTask')),
            ],
            options={
                'db_table': 'ingester_task_headers',
            },
        ),
        migrations.CreateModel(
            name='IngesterTaskParams',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('task', models.ForeignKey(to='ingester.IngesterTask')),
            ],
            options={
                'db_table': 'ingester_task_params',
            },
        ),
    ]
