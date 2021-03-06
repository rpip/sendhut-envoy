# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-20 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20190105_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepayment',
            name='channel',
            field=models.CharField(choices=[('wallet', 'wallet'), ('cash', 'cash')], max_length=32),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='channel',
            field=models.CharField(blank=True, choices=[('wallet', 'wallet'), ('cash', 'cash')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txn_type',
            field=models.CharField(choices=[('load-wallet', 'load wallet'), ('wallet-payment', 'payment')], max_length=32),
        ),
    ]
