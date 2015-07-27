# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0002_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesdatatype',
            name='category',
            field=models.IntegerField(choices=[(0, 'foods'), (1, 'activities'), (2, 'sleep'), (3, 'body')]),
            preserve_default=True,
        ),
    ]
