# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='This-slug'),
        ),
    ]