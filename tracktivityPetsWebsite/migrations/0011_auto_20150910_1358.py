# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0010_auto_20150910_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petswap',
            name='time_swapped',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 58, 57, 966362)),
        ),
        migrations.AlterField(
            model_name='usermicrochallenge',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 58, 57, 964362), null=True),
        ),
    ]
