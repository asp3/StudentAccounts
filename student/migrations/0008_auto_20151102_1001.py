# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_remove_userinfo_newfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='pin',
            field=models.DecimalField(max_digits=4, decimal_places=0),
        ),
    ]
