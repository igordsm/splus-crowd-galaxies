# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-06 13:19
from __future__ import unicode_literals

from django.db import migrations

def add_user_profile(apps, schema_editor):
    UserProfile = apps.get_model('core', 'Profile')
    User = apps.get_registered_model('auth', 'User')

    for usr in User.objects.all():
        usr.userprofile = UserProfile()
        usr.userprofile.save()
        usr.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_profile'),
    ]

    operations = [
        migrations.RunPython(add_user_profile)
    ]
