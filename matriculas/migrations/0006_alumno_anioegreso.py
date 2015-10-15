# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0005_auto_20151013_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='anioEgreso',
            field=models.IntegerField(null=True, verbose_name=b'A\xc3\xb1o de Egreso', blank=True),
        ),
    ]
