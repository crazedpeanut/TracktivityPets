# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0004_mood_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mood',
            old_name='name',
            new_name='description',
        ),
    ]
