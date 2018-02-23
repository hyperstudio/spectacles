# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-23 06:13
from __future__ import unicode_literals

import app.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datastore', '0002_annotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('annotation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='datastore.Annotation')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='datastore.Document')),
            ],
            bases=(app.utils.DictModel, models.Model),
        ),
        migrations.AddField(
            model_name='archive',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='archive',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
