# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-16 13:34
from __future__ import unicode_literals

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galaxyimage',
            name='image',
            field=models.ImageField(upload_to='galaxies/', verbose_name='Galaxy image'),
        ),
    ]
