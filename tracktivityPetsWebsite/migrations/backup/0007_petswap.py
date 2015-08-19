# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0006_auto_20150809_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetSwap',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('time_swapped', models.DateTimeField(auto_now=True)),
                ('from_pet', models.ForeignKey(related_name='from_pet', to='tracktivityPetsWebsite.CollectedPet')),
                ('to_pet', models.ForeignKey(related_name='to_pet', to='tracktivityPetsWebsite.CollectedPet')),
            ],
        ),
    ]
