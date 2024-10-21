# Generated by Django 5.1.2 on 2024-10-21 05:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_alter_cartridge_mfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridge',
            name='mfp',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.mfp', verbose_name='МФУ'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='ip_address',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='IP адрес'),
        ),
        migrations.AlterField(
            model_name='networkequipment',
            name='ip_address',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='IP адрес'),
        ),
        migrations.AlterField(
            model_name='server',
            name='ip_address',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='IP адрес'),
        ),
    ]
