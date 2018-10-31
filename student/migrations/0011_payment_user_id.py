# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_remove_payment_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
