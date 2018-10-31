# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_auto_20151103_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user_id',
        ),
    ]
