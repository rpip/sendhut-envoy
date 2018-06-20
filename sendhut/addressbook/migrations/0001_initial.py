# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-04 00:16
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import sendhut.db
import sendhut.utils
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('metadata', jsonfield.fields.JSONField(blank=True, max_length=360, null=True)),
                ('address', models.CharField(max_length=120)),
                ('apt', models.CharField(blank=True, max_length=42, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, null=True, srid=4326)),
                ('notes', models.CharField(blank=True, max_length=252, null=True)),
            ],
            options={
                'db_table': 'address',
            },
            bases=(models.Model, sendhut.db.UpdateMixin),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('metadata', jsonfield.fields.JSONField(blank=True, max_length=360, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=40, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addressbook.Address')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, sendhut.db.UpdateMixin),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('metadata', jsonfield.fields.JSONField(blank=True, max_length=360, null=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=sendhut.utils.image_upload_path)),
            ],
            options={
                'db_table': 'image',
            },
            bases=(models.Model, sendhut.db.UpdateMixin),
        ),
        migrations.AddField(
            model_name='address',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='addressbook.Image'),
        ),
    ]