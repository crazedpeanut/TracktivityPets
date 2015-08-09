# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0004_auto_20150809_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='scenery',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
