# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0002_auto_20150714_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petactive',
            name='endDateTime',
            field=models.DateTimeField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='petactive',
            name='stepsTakenDuringPeriod',
            field=models.IntegerField(default=0),
        ),
    ]
