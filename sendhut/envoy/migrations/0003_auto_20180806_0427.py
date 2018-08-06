# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-06 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('envoy', '0002_auto_20180625_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='envoy.Batch'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='envoy.DeliveryQuote'),
        ),
        migrations.AlterField(
            model_name='dropoff',
            name='package_type',
            field=models.CharField(choices=[('extra-small', 'Extra small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('extra-large', 'Extra large')], max_length=32),
        ),
    ]
