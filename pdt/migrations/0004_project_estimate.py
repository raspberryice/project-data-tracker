# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0003_auto_20151125_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='estimate',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
