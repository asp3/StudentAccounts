# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20151105_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoption',
            name='class_of',
        ),
        migrations.RemoveField(
            model_name='events',
            name='class_of',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='class_of',
        ),
    ]
