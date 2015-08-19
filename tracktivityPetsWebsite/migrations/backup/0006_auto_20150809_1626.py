# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0005_auto_20150809_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectedscenery',
            name='equipped_on',
        ),
        migrations.AddField(
            model_name='collectedpet',
            name='scenery',
            field=models.ForeignKey(null=True, to='tracktivityPetsWebsite.CollectedScenery'),
        ),
    ]
