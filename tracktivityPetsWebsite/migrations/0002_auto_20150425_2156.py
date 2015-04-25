# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mood',
            name='image',
        ),
        migrations.AddField(
            model_name='mood',
            name='image_location',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
