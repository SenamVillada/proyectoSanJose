# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0003_auto_20151009_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.CharField(default=b'masculino', max_length=16, verbose_name=b'Sexo', choices=[(b'masculino', b'Masculino'), (b'femenino', b'Femenino')]),
        ),
    ]
