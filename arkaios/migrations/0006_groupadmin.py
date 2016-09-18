# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkaios', '0005_groupgrades'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAdmin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('group', models.ForeignKey(to='arkaios.Group')),
            ],
        ),
    ]
