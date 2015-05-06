# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0005_auto_20150425_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_pet',
            field=models.OneToOneField(to='tracktivityPetsWebsite.CollectedPet', null=True),
        ),
    ]
