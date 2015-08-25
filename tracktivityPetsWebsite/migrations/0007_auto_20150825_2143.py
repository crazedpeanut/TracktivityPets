# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0006_microchallengegoal_medal_colour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microchallengegoal',
            name='medal_colour',
        ),
        migrations.AddField(
            model_name='microchallenge',
            name='challenge_type',
            field=models.CharField(null=True, max_length=100, choices=[('STEPS_IN_DURATION', 'STEPS_IN_DURATION')]),
        ),
    ]
