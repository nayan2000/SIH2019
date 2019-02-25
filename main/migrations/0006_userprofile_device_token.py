# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190223_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='device_token',
            field=models.CharField(max_length=260, null=True),
        ),
    ]
