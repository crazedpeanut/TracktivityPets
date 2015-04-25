# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0002_auto_20150425_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='mood',
            name='level',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Level', default=0),
            preserve_default=False,
        ),
    ]
