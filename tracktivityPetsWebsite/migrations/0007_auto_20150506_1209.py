# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0006_auto_20150505_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_fitbit_sync',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
