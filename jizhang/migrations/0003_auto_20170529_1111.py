# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 11:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jizhang', '0002_auto_20170525_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='类别名称'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='jizhang.Category', verbose_name='分类'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('user', 'name')]),
        ),
    ]
