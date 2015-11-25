# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0002_auto_20151120_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='totalDefects',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='totalSLOC',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='totalTime',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='iteration',
            name='status',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='phase',
            name='status',
            field=models.BooleanField(),
        ),
    ]
