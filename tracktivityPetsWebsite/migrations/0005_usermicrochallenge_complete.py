# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0004_auto_20150824_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermicrochallenge',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
