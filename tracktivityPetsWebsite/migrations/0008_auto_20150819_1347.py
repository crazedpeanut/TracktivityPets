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
        migrations.AlterField(
            model_name='collecteditem',
            name='equipped_on',
            field=models.ForeignKey(blank=True, to='tracktivityPetsWebsite.CollectedPet', null=True),
        ),
        migrations.DeleteModel(
            name='Usable',
        ),
    ]
