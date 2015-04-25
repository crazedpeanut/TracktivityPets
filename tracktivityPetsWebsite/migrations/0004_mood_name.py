# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0003_mood_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='mood',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
