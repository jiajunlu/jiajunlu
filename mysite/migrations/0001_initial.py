# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-31 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card24Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=30)),
                ('answer', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Card24Game_SavedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=30)),
                ('incache', models.BooleanField()),
            ],
        ),
    ]
