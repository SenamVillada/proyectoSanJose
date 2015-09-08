# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inasistencias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='amonestacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 5, 11, 35, 42, 624003)),
        ),
        migrations.AlterField(
            model_name='observacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 5, 11, 35, 42, 623159)),
        ),
    ]
