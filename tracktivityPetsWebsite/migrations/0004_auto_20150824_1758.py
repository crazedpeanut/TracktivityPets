# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0003_auto_20150824_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermicrochallenge',
            name='user',
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='profile',
            field=models.OneToOneField(null=True, to='tracktivityPetsWebsite.Profile'),
        ),
    ]
