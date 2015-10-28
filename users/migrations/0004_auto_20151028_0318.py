# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountLogin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('action_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'account_logins',
            },
        ),
        migrations.CreateModel(
            name='UserTokens',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('access_token', models.CharField(max_length=256)),
                ('valid_until', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'user_tokens',
            },
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
        migrations.AddField(
            model_name='usertokens',
            name='user',
            field=models.ForeignKey(to='users.User'),
        ),
        migrations.AddField(
            model_name='accountlogin',
            name='user',
            field=models.ForeignKey(to='users.User'),
        ),
    ]
