# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petactive',
            name='stepsTakenDuringPeriod',
            field=models.IntegerField(null=True, default=0),
        ),
    ]
