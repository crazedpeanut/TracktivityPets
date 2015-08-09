# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracktivityPetsWebsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_currently_equipped', models.BooleanField(default=False)),
                ('inventory', models.ForeignKey(to='tracktivityPetsWebsite.Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('experience_to_unlock', models.IntegerField()),
                ('image_location', models.TextField(default='')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallenge',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('overview', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallengeGoal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('pet_pennies_reward', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MicroChallengeMedal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('item_to_use', models.ForeignKey(to='tracktivityPetsWebsite.Item')),
                ('pet_usable_on', models.ForeignKey(to='tracktivityPetsWebsite.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='UserMicroChallenge',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('micro_challenge', models.ForeignKey(to='tracktivityPetsWebsite.MicroChallenge')),
            ],
        ),
        migrations.CreateModel(
            name='UserMicroChallengeState',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='collected_pet',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='story',
        ),
        migrations.RemoveField(
            model_name='mood',
            name='image',
        ),
        migrations.AddField(
            model_name='mood',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='mood',
            name='image_location',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='mood',
            name='level',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Level', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phrase',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='current_pet',
            field=models.OneToOneField(to='tracktivityPetsWebsite.CollectedPet', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_fitbit_sync',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='UserStory',
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
            model_name='collecteditem',
            name='item',
            field=models.ForeignKey(to='tracktivityPetsWebsite.Item'),
        ),
    ]