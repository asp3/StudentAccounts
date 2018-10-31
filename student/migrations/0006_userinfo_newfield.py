# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_userinfo_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='newfield',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
