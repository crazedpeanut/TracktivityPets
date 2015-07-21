# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0002_auto_20150720_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteditem',
            name='equipped_on',
            field=models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet', null=True),
        ),
    ]
