# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0003_auto_20160323_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='commitlog',
            name='repo_name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
