# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracktivityPetsWebsite', '0003_collecteditem_equipped_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedScenery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('equipped_on', models.ForeignKey(null=True, to='tracktivityPetsWebsite.CollectedPet')),
                ('inventory', models.ForeignKey(to='tracktivityPetsWebsite.Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='Scenery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('experience_to_unlock', models.IntegerField()),
                ('image_location', models.TextField(default='')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='collecteditem',
            name='is_currently_equipped',
        ),
        migrations.AddField(
            model_name='collectedscenery',
            name='scenery',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Scenery'),
        ),
    ]