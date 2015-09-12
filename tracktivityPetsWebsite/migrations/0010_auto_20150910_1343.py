# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0009_auto_20150826_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMicroChallengeGoalStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('complete', models.BooleanField(default=False)),
                ('micro_chal_goal', models.ForeignKey(to='tracktivityPetsWebsite.MicroChallengeGoal')),
            ],
        ),
        migrations.AddField(
            model_name='microchallenge',
            name='duration_mins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='date_completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='microchallenge',
            name='challenge_type',
            field=models.CharField(null=True, choices=[('steps_in_duration', 'STEPS_IN_DURATION')], max_length=100),
        ),
        migrations.AlterField(
            model_name='petswap',
            name='time_swapped',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 43, 20, 278730)),
        ),
        migrations.AlterField(
            model_name='usermicrochallenge',
            name='date_started',
            field=models.DateTimeField(null=True, default=datetime.datetime(2015, 9, 10, 13, 43, 20, 276730)),
        ),
        migrations.AlterField(
            model_name='usermicrochallenge',
            name='profile',
            field=models.ForeignKey(null=True, to='tracktivityPetsWebsite.Profile'),
        ),
        migrations.AddField(
            model_name='usermicrochallengegoalstatus',
            name='user_micro_chal',
            field=models.ForeignKey(to='tracktivityPetsWebsite.UserMicroChallenge'),
        ),
    ]
