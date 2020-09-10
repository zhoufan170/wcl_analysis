# Generated by Django 2.2.1 on 2020-08-30 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0004_auto_20200830_0721'),
    ]

    operations = [
        migrations.CreateModel(
            name='EyeTentacleDamage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ViscidusPoisonTick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage', models.IntegerField(default=0)),
                ('hit', models.IntegerField(default=0)),
                ('tick', models.IntegerField(default=0)),
                ('uptime', models.FloatField(default=0.0)),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Fight')),
                ('friendly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Friendly')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.WCLLog')),
            ],
        ),
    ]
