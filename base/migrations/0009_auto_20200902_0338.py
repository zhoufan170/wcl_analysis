# Generated by Django 2.2.1 on 2020-09-02 03:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20200902_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wcllog',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 3, 38, 24, 683836)),
        ),
    ]
