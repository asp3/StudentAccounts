# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_distribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='IOU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=30)),
                ('student_id', models.IntegerField()),
                ('class_of', models.CharField(max_length=20)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('last_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='cancel',
            name='class_of',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventoption',
            name='description',
            field=models.CharField(default='asdfasdfasdf', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventoption',
            name='class_of',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='events',
            name='class_of',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='class_of',
            field=models.CharField(max_length=20),
        ),
    ]
