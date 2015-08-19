# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0008_auto_20150819_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collecteditem',
            name='equipped_on',
        ),
        migrations.AddField(
            model_name='collecteditem',
            name='equipped',
            field=models.BooleanField(default=False),
        ),
    ]
