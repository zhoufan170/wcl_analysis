# Generated by Django 2.2.1 on 2020-08-30 13:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20200830_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wcllog',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 30, 13, 33, 58, 772711)),
        ),
    ]
