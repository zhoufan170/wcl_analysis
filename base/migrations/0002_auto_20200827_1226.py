# Generated by Django 2.2.1 on 2020-08-27 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enemy',
            old_name='guild',
            new_name='guid',
        ),
        migrations.RenameField(
            model_name='friendly',
            old_name='guild',
            new_name='guid',
        ),
    ]
