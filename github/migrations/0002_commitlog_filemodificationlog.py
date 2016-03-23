# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('github_id', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('sha', models.CharField(max_length=200)),
                ('additions', models.IntegerField()),
                ('deletions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FileModificationLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=50)),
                ('additions', models.IntegerField()),
                ('deletions', models.IntegerField()),
                ('file_name', models.CharField(max_length=200)),
                ('file_extension', models.CharField(max_length=20)),
                ('commit', models.ForeignKey(to='github.CommitLog')),
            ],
        ),
    ]
