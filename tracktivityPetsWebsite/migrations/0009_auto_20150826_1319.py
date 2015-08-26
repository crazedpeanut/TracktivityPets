# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0008_auto_20150825_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microchallengegoal',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='microchallengegoal',
            name='date_started',
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='date_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='date_started',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='microchallenge',
            name='challenge_type',
            field=models.CharField(choices=[(0, 'STEPS_IN_DURATION')], max_length=100, null=True),
        ),
    ]
