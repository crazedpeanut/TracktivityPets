# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0002_auto_20150820_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microchallengestate',
            name='date_started',
        ),
        migrations.AddField(
            model_name='microchallengegoal',
            name='date_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='microchallengegoal',
            name='date_started',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
