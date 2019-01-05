# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-05 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import sendhut.db


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_transaction_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePayment',
            fields=[
                ('id', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('metadata', jsonfield.fields.JSONField(blank=True, max_length=360, null=True)),
                ('channel', models.CharField(choices=[('wallet', 'wallet'), ('payment', 'payment')], max_length=32)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, sendhut.db.UpdateMixin),
        ),
        migrations.AddField(
            model_name='transaction',
            name='channel',
            field=models.CharField(blank=True, choices=[('wallet', 'wallet'), ('payment', 'payment')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='payments.Wallet'),
        ),
    ]
