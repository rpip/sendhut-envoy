# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-03 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reference',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]