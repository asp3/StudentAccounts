# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_payment_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('date', models.DateTimeField(auto_now=True)),
                ('event', models.CharField(max_length=25)),
                ('user_id', models.IntegerField()),
                ('quantity', models.DecimalField(max_digits=3, decimal_places=0)),
                ('price_of_each', models.DecimalField(max_digits=5, decimal_places=2)),
                ('total_cost', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
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
