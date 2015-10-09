# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0002_auto_20151009_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.CharField(default=b'masculino', max_length=16, verbose_name=b'Sexo', choices=[(b'casado', b'Casado/a'), (b'soltero', b'Soltero/a'), (b'viudo', b'Viudo/a'), (b'divorciado', b'Divorciado/a')]),
        ),
    ]
