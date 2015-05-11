# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0007_auto_20150506_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstory',
            name='collected_pet',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='story',
        ),
        migrations.DeleteModel(
            name='UserStory',
        ),
    ]
