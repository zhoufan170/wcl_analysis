# Generated by Django 2.2.1 on 2020-09-02 05:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20200902_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wcllog',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 5, 45, 17, 728217)),
        ),
    ]
