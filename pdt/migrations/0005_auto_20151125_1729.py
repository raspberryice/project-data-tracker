# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0004_project_estimate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='estimate',
            new_name='slocestimate',
        ),
        migrations.AddField(
            model_name='project',
            name='efforestimate',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
