# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('reincorporacion', models.IntegerField(default=0, max_length=2, verbose_name=b'Reincorporacion')),
                ('dni', models.IntegerField(max_length=100, verbose_name=b'Dni')),
            ],
            options={
                'verbose_name': 'alumno',
                'verbose_name_plural': 'alumnos',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Amonestacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(max_length=2, verbose_name=b'Cantidad')),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateField(default=datetime.datetime(2014, 12, 1, 10, 30, 3, 434017))),
                ('alumno', models.ForeignKey(to='inasistencias.Alumno')),
            ],
            options={
                'verbose_name_plural': 'amonestaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(max_length=1, verbose_name=b'Curso')),
                ('division', models.CharField(max_length=1, verbose_name=b'Division')),
                ('anio', models.IntegerField(max_length=4, verbose_name=b'Ciclo lectivo')),
            ],
            options={
                'ordering': ('-anio', 'numero', 'division'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inasistencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.FloatField()),
                ('justificado', models.BooleanField(default=False)),
                ('fecha', models.DateField()),
                ('alumno', models.ForeignKey(to='inasistencias.Alumno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateField(default=datetime.datetime(2014, 12, 1, 10, 30, 3, 433218))),
                ('alumno', models.ForeignKey(to='inasistencias.Alumno')),
            ],
            options={
                'verbose_name_plural': 'observaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Preceptor',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cursos', models.ManyToManyField(to='inasistencias.Curso')),
            ],
            options={
                'verbose_name': 'preceptor',
                'verbose_name_plural': 'preceptores',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='observacion',
            name='preceptor',
            field=models.ForeignKey(to='inasistencias.Preceptor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inasistencia',
            name='preceptor',
            field=models.ForeignKey(to='inasistencias.Preceptor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='amonestacion',
            name='preceptor',
            field=models.ForeignKey(to='inasistencias.Preceptor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(to='inasistencias.Curso'),
            preserve_default=True,
        ),
    ]
