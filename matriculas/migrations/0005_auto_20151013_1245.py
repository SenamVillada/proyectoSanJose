# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0004_auto_20151009_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='correlativasCursado',
            field=models.ManyToManyField(related_name='_correlativasCursado_+', to='matriculas.Materia', blank=True),
        ),
        migrations.AlterField(
            model_name='materia',
            name='correlativasRendir',
            field=models.ManyToManyField(related_name='_correlativasRendir_+', to='matriculas.Materia', blank=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='curriculum',
            field=models.FileField(upload_to=b'curriculums/%Y/%m', verbose_name=b'Curriculum', blank=True),
        ),
    ]
