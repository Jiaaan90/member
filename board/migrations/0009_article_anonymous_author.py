# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-13 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_auto_20200212_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='anonymous_author',
            field=models.CharField(max_length=100, null=True, verbose_name='\uc791\uc131\uc790'),
        ),
    ]
