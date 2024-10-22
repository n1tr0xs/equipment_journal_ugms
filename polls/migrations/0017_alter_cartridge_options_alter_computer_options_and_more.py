# Generated by Django 5.1.2 on 2024-10-22 11:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_alter_cartridge_number_alter_computer_comment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartridge',
            options={'verbose_name': 'Картридж', 'verbose_name_plural': 'Картриджы'},
        ),
        migrations.AlterModelOptions(
            name='computer',
            options={'verbose_name': 'Компьютер', 'verbose_name_plural': 'Компьютеры'},
        ),
        migrations.AlterModelOptions(
            name='computerconfiguration',
            options={'verbose_name': 'Конфигурация (сборка) компьютера', 'verbose_name_plural': 'Конфигурации (сборки) компьютеров'},
        ),
        migrations.AlterModelOptions(
            name='meteounit',
            options={'verbose_name': 'Прибор (гидро / метео / агро)', 'verbose_name_plural': 'Приборы (гидро / метео / агро)'},
        ),
        migrations.AlterModelOptions(
            name='mfp',
            options={'verbose_name': 'МФУ', 'verbose_name_plural': 'МФУ'},
        ),
        migrations.AlterModelOptions(
            name='monitor',
            options={'verbose_name': 'Монитор', 'verbose_name_plural': 'Мониторы'},
        ),
        migrations.AlterModelOptions(
            name='networkequipment',
            options={'verbose_name': 'Сетевое оборудование', 'verbose_name_plural': 'Сетевое оборудование'},
        ),
        migrations.AlterModelOptions(
            name='peripheral',
            options={'verbose_name': 'Периферия', 'verbose_name_plural': 'Периферия'},
        ),
        migrations.AlterModelOptions(
            name='peripheraltype',
            options={'verbose_name': 'Тип периферии', 'verbose_name_plural': 'Типы периферии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Должность', 'verbose_name_plural': 'Должности'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name': 'Запрос', 'verbose_name_plural': 'Запросы'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'verbose_name': 'Сервер', 'verbose_name_plural': 'Сервера'},
        ),
        migrations.AlterModelOptions(
            name='ups',
            options={'verbose_name': 'ИБП', 'verbose_name_plural': 'ИБП'},
        ),
        migrations.AlterModelOptions(
            name='worksite',
            options={'verbose_name': 'Рабочее место', 'verbose_name_plural': 'Рабочие места'},
        ),
        migrations.AlterField(
            model_name='computer',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='meteounit',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.structure', verbose_name='Структура'),
        ),
        migrations.AlterField(
            model_name='mfp',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='networkequipment',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.structure', verbose_name='Структура'),
        ),
        migrations.AlterField(
            model_name='peripheral',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='post',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.structure', verbose_name='Структура'),
        ),
        migrations.AlterField(
            model_name='request',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Выполнен'),
        ),
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Создан'), (1, 'В работе'), (2, 'Выполнен')], default=0, verbose_name='Статус запроса'),
        ),
        migrations.AlterField(
            model_name='request',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='server',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.structure', verbose_name='Структура'),
        ),
        migrations.AlterField(
            model_name='ups',
            name='worksite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worksite', verbose_name='Рабочее место'),
        ),
        migrations.AlterField(
            model_name='worksite',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.post', verbose_name='Должность'),
        ),
    ]
