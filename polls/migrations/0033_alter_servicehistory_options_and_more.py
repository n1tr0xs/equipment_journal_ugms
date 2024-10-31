# Generated by Django 5.1.2 on 2024-10-31 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_alter_cartridge_device_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicehistory',
            options={'verbose_name': 'История обслуживания', 'verbose_name_plural': 'История обслуживания'},
        ),
        migrations.AlterField(
            model_name='cartridge',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=8, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=1, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='meteounit',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=6, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='mfp',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=2, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=4, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='networkequipment',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=3, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='peripheral',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=0, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='server',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=7, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='ups',
            name='device_type',
            field=models.IntegerField(choices=[(0, 'Периферия'), (1, 'Комьютер'), (2, 'МФУ'), (3, 'Сетевое оборудование'), (4, 'Монитор'), (5, 'ИБП'), (6, 'Прибор'), (7, 'Сервер'), (8, 'Картридж')], default=5, verbose_name='Тип устройства'),
        ),
    ]
