# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20151105_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoption',
            name='class_of',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='events',
            name='class_of',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='class_of',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
