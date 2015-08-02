# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=100)),
                ('date_created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet')),
            ],
        ),
        migrations.CreateModel(
            name='Happiness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(unique=True)),
                ('experience_needed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('happiness_needed', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_name', models.CharField(max_length=100)),
                ('experience_to_unlock', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('starter_level', models.ForeignKey(to='tracktivityPetsWebsite.Level')),
            ],
        ),
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('mood', models.ForeignKey(to='tracktivityPetsWebsite.Mood')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_pet_pennies', models.IntegerField(default=0)),
                ('last_fitbit_sync', models.DateTimeField(null=True)),
                ('current_pet', models.OneToOneField(to='tracktivityPetsWebsite.CollectedPet')),
                ('inventory', models.OneToOneField(to='tracktivityPetsWebsite.Inventory')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('level_unlocked', models.ForeignKey(to='tracktivityPetsWebsite.Level')),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_viewed', models.BooleanField(default=False)),
                ('collected_pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet')),
                ('story', models.ForeignKey(to='tracktivityPetsWebsite.Story')),
            ],
        ),
        migrations.AddField(
            model_name='mood',
            name='pet',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Pet'),
        ),
        migrations.AddField(
            model_name='collectedpet',
            name='inventory',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Inventory'),
        ),
        migrations.AddField(
            model_name='collectedpet',
            name='level',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Level'),
        ),
        migrations.AddField(
            model_name='collectedpet',
            name='pet',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Pet'),
        ),
    ]
