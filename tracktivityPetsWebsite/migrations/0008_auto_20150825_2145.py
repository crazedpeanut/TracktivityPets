# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0007_auto_20150825_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='belongs_to',
            field=models.ForeignKey(null=True, to='tracktivityPetsWebsite.Pet'),
        ),
    ]
