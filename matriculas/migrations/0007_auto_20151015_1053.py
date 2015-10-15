# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0006_alumno_anioegreso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'verbose_name': 'Alumno', 'verbose_name_plural': 'Alumnos'},
        ),
        migrations.AlterModelOptions(
            name='profesor',
            options={'verbose_name': 'Profesor', 'verbose_name_plural': 'Profesores'},
        ),
        migrations.AddField(
            model_name='matricula',
            name='finalizada',
            field=models.BooleanField(default=b'False', verbose_name=b'Finalizada?'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(verbose_name=b'Fecha'),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='anio',
            field=models.IntegerField(verbose_name=b'A\xc3\xb1o'),
        ),
    ]
