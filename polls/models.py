from django.db import models
from django.urls import reverse

# Create your models here.


class NamedEntity(models.Model):
    class Meta:
        abstract = True
        ordering = ['name']

    name = models.CharField(max_length=100, default='', verbose_name='Название')

    def __str__(self):
        return f'{self.name}'


class IPEntity(models.Model):
    class Meta:
        abstract = True

    ip_address = models.CharField(max_length=15, verbose_name='IP адрес', null=True, blank=True)


class Inventoried(models.Model):
    class Meta:
        abstract = True

    inventory_number = models.CharField(max_length=50, unique=True, default='', verbose_name='Инвентарный номер')
    serial_number = models.CharField(max_length=50, unique=True, default='', verbose_name='Серийный номер')


class TechnicalConditionEntity(models.Model):
    class Meta:
        abstract = True
        ordering = ['technical_condition']

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


class Post(NamedEntity):
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name', 'structure']

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')


class Worksite(NamedEntity):
    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'
        ordering = ['name', 'post']

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Должность')


class WorksitePlaced(models.Model):
    class Meta:
        abstract = True
        ordering = ['worksite']

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class StructurePlaced(models.Model):
    class Meta:
        abstract = True
        ordering = ['structure']

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


class PeripheralType(NamedEntity):
    class Meta:
        verbose_name = 'Тип периферии'
        verbose_name_plural = 'Типы периферии'
        ordering = ['name']


class ComputerConfiguration(NamedEntity):
    class Meta:
        verbose_name = 'Конфигурация (сборка) компьютера'
        verbose_name_plural = 'Конфигурации (сборки) компьютеров'
        ordering = ['name']

    processor = models.CharField(max_length=50, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    motherboard = models.CharField(max_length=50, verbose_name='Материнская плата')
    drives = models.TextField(verbose_name='Накопители')
    power_supply = models.CharField(max_length=50, verbose_name='Блок питания')


class Peripheral(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'Периферия'
        verbose_name_plural = 'Периферия'
        ordering = ['name', 'peripheral_type']

    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип периферии')


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'
        ordering = ['name', 'technical_condition', 'structure', 'ip_address']


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced, IPEntity):
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'
        ordering = ['name', 'technical_condition', 'worksite', 'ip_address']

    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')
    comment = models.CharField(max_length=100, verbose_name='Комменарий', null=True, blank=True)


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'
        ordering = ['name', 'technical_condition', 'worksite']


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'МФУ'
        verbose_name_plural = 'МФУ'
        ordering = ['name', 'technical_condition', 'worksite']


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'ИБП'
        verbose_name_plural = 'ИБП'
        ordering = ['name', 'technical_condition', 'worksite']


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    class Meta:
        verbose_name = 'Прибор (гидро / метео / агро)'
        verbose_name_plural = 'Приборы (гидро / метео / агро)'
        ordering = ['name', 'technical_condition', 'structure']
    verification_date = models.DateField(verbose_name='Дата поверки', null=True)


class Server(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'
        ordering = ['name', 'technical_condition', 'structure', 'ip_address']

    purpose = models.TextField(default='', verbose_name='Назначение')


class Cartridge(NamedEntity, TechnicalConditionEntity):
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджы'
        ordering = ['name', 'technical_condition', 'refills']

    mfp = models.ForeignKey(MFP, on_delete=models.CASCADE, verbose_name='МФУ', null=True, blank=True)
    number = models.CharField(max_length=50, verbose_name='Номер картриджа', default='')
    refills = models.PositiveIntegerField(default=0, verbose_name='Количество заправок')

    def get_absolute_url(self):
        return reverse('cartridge-detail', kwargs={'pk': self.pk})


class Request(WorksitePlaced):
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ['status', 'created_at', 'completed_at']

    class RequestStatus(models.IntegerChoices):
        CREATED = 0, 'Создан'
        IN_WORK = 1, 'В работе'
        COMPLETED = 2, 'Выполнен'

    description = models.TextField(default='', verbose_name='Описание запроса')
    status = models.IntegerField(choices=RequestStatus, verbose_name='Статус запроса', default=RequestStatus.CREATED)
    created_at = models.DateTimeField(null=True, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, verbose_name='Выполнен')
