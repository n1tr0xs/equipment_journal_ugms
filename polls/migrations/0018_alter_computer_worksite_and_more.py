# Generated by Django 5.1.2 on 2024-10-23 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_alter_cartridge_options_alter_computer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='meteounit',
            name='verification_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата поверки'),
        ),
        migrations.AlterField(
            model_name='mfp',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='peripheral',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='request',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='server',
            name='purpose',
            field=models.TextField(blank=True, default='', verbose_name='Назначение'),
        ),
        migrations.AlterField(
            model_name='ups',
            name='worksite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
    ]
