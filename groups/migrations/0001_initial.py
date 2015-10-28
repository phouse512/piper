# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151028_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('group', models.ForeignKey(to='groups.Group')),
                ('user', models.ForeignKey(to='users.User')),
            ],
            options={
                'db_table': 'groups_membership',
            },
        ),
    ]
