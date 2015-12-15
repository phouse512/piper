# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151028_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubIntegration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('github_id', models.CharField(max_length=50)),
                ('github_username', models.CharField(max_length=120)),
                ('oauth_token', models.CharField(max_length=256)),
                ('expires_at', models.DateTimeField()),
                ('oauth_is_valid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='users.User')),
            ],
            options={
                'db_table': 'github_integrations',
            },
        ),
    ]
