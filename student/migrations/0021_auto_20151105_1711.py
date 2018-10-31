# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_auto_20151105_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancel',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='iou',
            name='last_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='pub_date',
            field=models.DateField(auto_now=True),
        ),
    ]
