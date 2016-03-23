# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0002_commitlog_filemodificationlog'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='commitlog',
            table='commit_log',
        ),
        migrations.AlterModelTable(
            name='filemodificationlog',
            table='file_modification_log',
        ),
    ]
