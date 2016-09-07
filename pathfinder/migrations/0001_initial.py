# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('weight', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('able_to', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NodeResources',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('node', models.ForeignKey(to='pathfinder.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('link', models.TextField()),
                ('how_to', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='noderesources',
            name='resource',
            field=models.ForeignKey(to='pathfinder.Resource'),
        ),
        migrations.AddField(
            model_name='node',
            name='resources',
            field=models.ManyToManyField(to='pathfinder.Resource', through='pathfinder.NodeResources'),
        ),
        migrations.AddField(
            model_name='edge',
            name='dest',
            field=models.ForeignKey(related_name='dest_edge', to='pathfinder.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(related_name='source_edge', to='pathfinder.Node'),
        ),
    ]
