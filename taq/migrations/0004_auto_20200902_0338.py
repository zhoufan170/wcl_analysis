# Generated by Django 2.2.1 on 2020-09-02 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taq', '0003_bossnatureprotection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bossnatureprotection',
            name='major_nature_protection_uptime',
            field=models.FloatField(),
        ),
    ]
