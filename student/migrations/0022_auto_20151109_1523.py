# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_auto_20151105_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('event_date', models.DateField(default=datetime.date.today)),
                ('cost', models.DecimalField(max_digits=6, decimal_places=2)),
                ('description', models.CharField(max_length=500)),
                ('class_of', models.CharField(max_length=20)),
                ('regular_lunch', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='eventoption',
            name='event',
        ),
        migrations.RemoveField(
            model_name='cancel',
            name='date',
        ),
        migrations.RemoveField(
            model_name='events',
            name='date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.AddField(
            model_name='cancel',
            name='cancel_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='events',
            name='event_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='events',
            name='regular_lunch',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default='asdfasdf', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='first_name',
            field=models.CharField(default='asdfasdf', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='last_name',
            field=models.CharField(default='asdfasdf', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='iou',
            name='last_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='pub_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.DeleteModel(
            name='EventOption',
        ),
    ]
