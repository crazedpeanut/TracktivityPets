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
            name='BodyPart',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CollectedItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('equipped', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CollectedPet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, default=None)),
                ('date_created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CollectedScenery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet')),
            ],
        ),
        migrations.CreateModel(
            name='Happiness',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('experience_to_unlock', models.IntegerField()),
                ('image_location', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('level', models.IntegerField(unique=True)),
                ('experience_needed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallenge',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('overview', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallengeGoal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('description', models.TextField(default='')),
                ('pet_pennies_reward', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallengeMedal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallengeState',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_started', models.DateTimeField(auto_now=True)),
                ('steps', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('happiness_needed', models.IntegerField()),
                ('image_location', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('level', models.ForeignKey(to='tracktivityPetsWebsite.Level')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('default_name', models.CharField(max_length=100)),
                ('experience_to_unlock', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('starter_level', models.ForeignKey(to='tracktivityPetsWebsite.Level')),
            ],
        ),
        migrations.CreateModel(
            name='PetSwap',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time_swapped', models.DateTimeField(auto_now=True)),
                ('from_pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet', related_name='from_pet')),
                ('to_pet', models.ForeignKey(to='tracktivityPetsWebsite.CollectedPet', related_name='to_pet')),
            ],
        ),
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(default='')),
                ('mood', models.ForeignKey(to='tracktivityPetsWebsite.Mood')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('total_pet_pennies', models.IntegerField(default=0)),
                ('last_fitbit_sync', models.DateTimeField(null=True, blank=True)),
                ('current_pet', models.OneToOneField(null=True, to='tracktivityPetsWebsite.CollectedPet')),
                ('inventory', models.OneToOneField(to='tracktivityPetsWebsite.Inventory')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scenery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('experience_to_unlock', models.IntegerField()),
                ('image_location', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(default='')),
                ('level_unlocked', models.ForeignKey(to='tracktivityPetsWebsite.Level')),
                ('pet', models.ForeignKey(to='tracktivityPetsWebsite.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='UserMicroChallenge',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('micro_challenge', models.ForeignKey(to='tracktivityPetsWebsite.MicroChallenge')),
            ],
        ),
        migrations.CreateModel(
            name='UserMicroChallengeState',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.ForeignKey(to='tracktivityPetsWebsite.MicroChallengeState')),
            ],
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='state',
            field=models.ForeignKey(to='tracktivityPetsWebsite.UserMicroChallengeState'),
        ),
        migrations.AddField(
            model_name='usermicrochallenge',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mood',
            name='pet',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Pet'),
        ),
        migrations.AddField(
            model_name='microchallengegoal',
            name='goal_state',
            field=models.ForeignKey(to='tracktivityPetsWebsite.MicroChallengeState'),
        ),
        migrations.AddField(
            model_name='microchallengegoal',
            name='medal',
            field=models.ForeignKey(to='tracktivityPetsWebsite.MicroChallengeMedal'),
        ),
        migrations.AddField(
            model_name='microchallengegoal',
            name='micro_challenge',
            field=models.ForeignKey(to='tracktivityPetsWebsite.MicroChallenge'),
        ),
        migrations.AddField(
            model_name='item',
            name='belongs_to',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Pet'),
        ),
        migrations.AddField(
            model_name='item',
            name='body_part',
            field=models.ForeignKey(to='tracktivityPetsWebsite.BodyPart'),
        ),
        migrations.AddField(
            model_name='collectedscenery',
            name='inventory',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Inventory'),
        ),
        migrations.AddField(
            model_name='collectedscenery',
            name='scenery',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Scenery'),
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
        migrations.AddField(
            model_name='collectedpet',
            name='scenery',
            field=models.ForeignKey(null=True, to='tracktivityPetsWebsite.CollectedScenery'),
        ),
        migrations.AddField(
            model_name='collecteditem',
            name='inventory',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Inventory'),
        ),
        migrations.AddField(
            model_name='collecteditem',
            name='item',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Item'),
        ),
    ]
