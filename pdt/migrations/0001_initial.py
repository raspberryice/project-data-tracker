# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManageSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('iteration', models.ForeignKey(to='pdt.Iteration')),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('developer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no', models.IntegerField(default=1, choices=[(1, b'Inception'), (2, b'Elaboration'), (3, b'Construction'), (4, b'Migration')])),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(choices=[(1, b'Developer'), (2, b'Manager')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SLOCSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('developer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('iteration', models.ForeignKey(to='pdt.Iteration')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='participate',
            name='project',
            field=models.ForeignKey(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='phase',
            field=models.ForeignKey(to='pdt.Phase'),
        ),
    ]
