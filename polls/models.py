from datetime import datetime

from django.urls import reverse
from django.db import models


class NamedEntity(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, default='', verbose_name='Название')

    def __str__(self):
        return f'{self.name}'


class IPEntity(models.Model):
    class Meta:
        abstract = True

    ip_address = models.CharField(max_length=15, verbose_name='IP адрес', null=True, blank=True, unique=True)


class Inventoried(models.Model):
    class Meta:
        abstract = True

    inventory_number = models.CharField(max_length=50, unique=True, default='', verbose_name='Инвентарный номер')
    serial_number = models.CharField(max_length=50, unique=True, default='', verbose_name='Серийный номер')


class TechnicalConditionEntity(models.Model):
    class Meta:
        abstract = True

    class TechnicalCondition(models.IntegerChoices):
        READY_TO_USE = 0, 'Готов к установке'
        IN_WORK = 1, 'В работе'
        DISABLED = 2, 'Снят'
        REPAIRING = 3, 'Ремонт'

    technical_condition = models.IntegerField(choices=TechnicalCondition, verbose_name='Техническое состояние', default=TechnicalCondition.READY_TO_USE)
    disabling_reason = models.TextField(default='', verbose_name='Причина снятия', blank=True)


class Structure(NamedEntity):
    class Meta:
        verbose_name = 'Структура'
        verbose_name_plural = 'Структуры'

    physical_place = models.TextField(verbose_name='Физическое расположение')


class StructurePlaced(models.Model):
    class Meta:
        abstract = True

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


class Post(NamedEntity, StructurePlaced):
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return f'{self.name}'


class Worksite(NamedEntity):
    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Должность', null=True, blank=True)


class WorksitePlaced(models.Model):
    class Meta:
        abstract = True

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True)


class PeripheralType(NamedEntity):
    class Meta:
        verbose_name = 'Тип периферии'
        verbose_name_plural = 'Типы периферии'


class ComputerConfiguration(NamedEntity):
    class Meta:
        verbose_name = 'Конфигурация (сборка) компьютера'
        verbose_name_plural = 'Конфигурации (сборки) компьютеров'

    processor = models.CharField(max_length=50, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    motherboard = models.CharField(max_length=50, verbose_name='Материнская плата')
    drives = models.TextField(verbose_name='Накопители')
    power_supply = models.CharField(max_length=50, verbose_name='Блок питания')


class Peripheral(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'Периферия'
        verbose_name_plural = 'Периферия'

    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип периферии')

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'

    def __str__(self):
        return f'{self.name} {self.ip_address}'


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced, IPEntity):
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'

    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')
    comment = models.CharField(max_length=100, verbose_name='Комменарий', default='', blank=True)

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'МФУ'
        verbose_name_plural = 'МФУ'

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'ИБП'
        verbose_name_plural = 'ИБП'

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    class Meta:
        verbose_name = 'Прибор (гидро / метео / агро)'
        verbose_name_plural = 'Приборы (гидро / метео / агро)'

    verification_date = models.DateField(verbose_name='Дата поверки', null=True)

    def __str__(self):
        return f'{self.name}, {self.structure}'


class Server(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'

    purpose = models.TextField(default='', verbose_name='Назначение')

    def __str__(self):
        return f'{self.name} - {self.ip_address}'


class Cartridge(NamedEntity, TechnicalConditionEntity):
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджы'

    mfp = models.OneToOneField(MFP, on_delete=models.CASCADE, verbose_name='МФУ', null=True, blank=True)
    number = models.CharField(max_length=50, verbose_name='Номер картриджа', default='', null=True, blank=True, unique=True)
    refills = models.PositiveIntegerField(default=0, verbose_name='Количество заправок')

    def __str__(self):
        return f'{self.name} {self.mfp}'


class Request(WorksitePlaced):
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    class RequestStatus(models.IntegerChoices):
        CREATED = 0, 'Создан'
        IN_WORK = 1, 'В работе'
        COMPLETED = 2, 'Выполнен'

    description = models.TextField(default='', verbose_name='Описание запроса')
    status = models.IntegerField(choices=RequestStatus, verbose_name='Статус запроса', default=RequestStatus.CREATED, blank=True)
    created_at = models.DateTimeField(default=datetime.now, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, verbose_name='Выполнен', blank=True)

    def get_absolute_url(self):
        return reverse('request-detail', kwargs={'pk': self.pk})
