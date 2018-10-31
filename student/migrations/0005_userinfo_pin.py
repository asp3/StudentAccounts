# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20151030_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='pin',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
