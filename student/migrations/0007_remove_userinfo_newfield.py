# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_userinfo_newfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='newfield',
        ),
    ]
