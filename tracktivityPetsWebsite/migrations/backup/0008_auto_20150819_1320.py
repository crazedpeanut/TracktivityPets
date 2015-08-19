# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0007_petswap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usable',
            name='item_to_use',
        ),
        migrations.RemoveField(
            model_name='usable',
            name='pet_usable_on',
        ),
        migrations.RemoveField(
            model_name='collecteditem',
            name='equipped_on',
        ),
        migrations.AddField(
            model_name='collecteditem',
            name='equipped',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Usable',
        ),
    ]
