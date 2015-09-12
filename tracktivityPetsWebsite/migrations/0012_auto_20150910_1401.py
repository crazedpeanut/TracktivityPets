# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0011_auto_20150910_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petswap',
            name='time_swapped',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 14, 1, 20, 348506)),
        ),
        migrations.AlterField(
            model_name='usermicrochallenge',
            name='date_started',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
