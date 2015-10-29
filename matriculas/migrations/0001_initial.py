# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now=True, verbose_name=b'Fecha')),
                ('vino', models.BooleanField(verbose_name=b'Vino?')),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20, verbose_name=b'Nombre')),
                ('fechaAlta', models.DateField(verbose_name=b'Fecha de Alta')),
                ('fechaBaja', models.DateField(verbose_name=b'Fecha de Baja')),
            ],
        ),
        migrations.CreateModel(
            name='Licencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Alta')),
                ('fechaFinal', models.DateField(verbose_name=b'Fecha de Baja')),
                ('motivo', models.CharField(max_length=200, verbose_name=b'Motivo')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(verbose_name=b'Fecha')),
                ('log', models.CharField(max_length=200, verbose_name=b'Log')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30, verbose_name=b'Nombre de la Materia')),
                ('tipo', models.CharField(default=b'asignatura', max_length=80, verbose_name=b'Tipo de Materia', choices=[(b'asignatura', b'Asignatura'), (b'seminario', b'Seminario'), (b'taller', b'Taller')])),
                ('correlativasCursado', models.ManyToManyField(related_name='_correlativasCursado_+', to='matriculas.Materia')),
                ('correlativasRendir', models.ManyToManyField(related_name='_correlativasRendir_+', to='matriculas.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anio', models.DateField(auto_now=True)),
                ('horario', models.CharField(max_length=200, verbose_name=b'Horario')),
                ('aprobada', models.BooleanField(verbose_name=b'Aprobada?')),
                ('materia', models.ForeignKey(to='matriculas.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now=True, verbose_name=b'Fecha')),
                ('calificacion', models.IntegerField(verbose_name=b'Calificacion')),
                ('observacion', models.CharField(max_length=100, verbose_name=b'Observacion')),
                ('matricula', models.ForeignKey(to='matriculas.Matricula')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.IntegerField(verbose_name=b'DNI')),
                ('domicilio', models.CharField(max_length=300, verbose_name=b'Domicilio')),
                ('estadoCivil', models.CharField(default=b'soltero', max_length=16, verbose_name=b'Estado Civil', choices=[(b'casado', b'Casado/a'), (b'soltero', b'Soltero/a'), (b'viudo', b'Viudo/a'), (b'divorciado', b'Divorciado/a')])),
                ('fechaNacimiento', models.DateField(verbose_name=b'Fecha de Nacimiento')),
                ('lugarNacimiento', models.CharField(max_length=50, verbose_name=b'Lugar de Nacimiento')),
                ('telefonoFijo', models.IntegerField(verbose_name=b'Telefono Fijo')),
                ('telefonoMovil', models.IntegerField(verbose_name=b'Telefono Celular')),
                ('sexo', models.CharField(max_length=1, verbose_name=b'Sexo')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='matriculas.Persona')),
                ('lugarDeTrabajo', models.CharField(max_length=50, verbose_name=b'Lugar de Trabajo')),
                ('horaDeTrabajo', models.CharField(max_length=200, verbose_name=b'Horario de Trabajo')),
                ('paternidad', models.BooleanField(verbose_name=b'Paternidad')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('matriculas.persona',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='matriculas.Persona')),
                ('cuil', models.IntegerField(verbose_name=b'CUIL')),
                ('curriculum', models.FileField(upload_to=b'curriculums/%Y/%m', verbose_name=b'Curriculum')),
                ('fechaEscalafon', models.DateField(verbose_name=b'Fecha de Escalafon')),
                ('fechaAptoPsicofisico', models.DateField(verbose_name=b'Fecha del Apto Psicofisico')),
                ('numeroRegistro', models.IntegerField(verbose_name=b'Numero de Registro')),
                ('titulo', models.CharField(max_length=200, verbose_name=b'Titulo')),
                ('cargo', models.ForeignKey(to='matriculas.Cargo')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('matriculas.persona',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='asistencia',
            name='matricula',
            field=models.ForeignKey(to='matriculas.Matricula'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='alumno',
            field=models.ForeignKey(to='matriculas.Alumno'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='profesor',
            field=models.ForeignKey(to='matriculas.Profesor'),
        ),
        migrations.AddField(
            model_name='licencia',
            name='profesor',
            field=models.ForeignKey(to='matriculas.Profesor'),
        ),
    ]
