# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20151102_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option_text', models.CharField(max_length=50)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
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
            model_name='events',
            name='description',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventoption',
            name='event',
            field=models.ForeignKey(to='student.Events'),
        ),
    ]
