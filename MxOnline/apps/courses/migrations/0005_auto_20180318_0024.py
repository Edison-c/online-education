# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-18 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20180317_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresource',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='\u8bfe\u7a0b'),
        ),
    ]