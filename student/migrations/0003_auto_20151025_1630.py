# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_userinfo_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('date', models.DateTimeField()),
                ('cost', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=2),
            preserve_default=False,
        ),
    ]
