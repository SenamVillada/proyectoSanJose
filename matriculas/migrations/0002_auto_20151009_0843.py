# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='correlativasCursado',
            field=models.ManyToManyField(related_name='_correlativasCursado_+', null=True, to='matriculas.Materia', blank=True),
        ),
        migrations.AlterField(
            model_name='materia',
            name='correlativasRendir',
            field=models.ManyToManyField(related_name='_correlativasRendir_+', null=True, to='matriculas.Materia', blank=True),
        ),
    ]
