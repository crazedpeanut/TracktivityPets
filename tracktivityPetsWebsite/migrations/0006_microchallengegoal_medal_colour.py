# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0005_usermicrochallenge_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='microchallengegoal',
            name='medal_colour',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
