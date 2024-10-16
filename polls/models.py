from django.db import models

# Create your models here.


class NamedEntity(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, default='', verbose_name='Название')

    def __str__(self):
        return f'{self.name}'


class Inventoried(models.Model):
    '''
    Родительский класс для классов с инвентарным номером и серийным номером.
    '''
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
    '''
    Струтурное подразделения.
    '''
    class Meta:
        verbose_name = 'Структура'
        verbose_name_plural = 'Структуры'

    physical_place = models.TextField(verbose_name='Физическое расположение')


class Post(NamedEntity):
    '''
    Должность работника.
    '''
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')


class Worksite(NamedEntity):
    '''
    Рабочее место.
    '''
    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Должность')


class WorksitePlaced(models.Model):
    '''
    Базовый класс для оборудования, привязанного к рабочему месту
    '''
    class Meta:
        abstract = True

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class StructurePlaced(models.Model):
    '''
    Базовый класс для оборудования, привязанного к рабочему месту
    '''
    class Meta:
        abstract = True

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


class PeripheralType(NamedEntity):
    '''
    Тип переферии.
    '''
    class Meta:
        verbose_name = 'Тип периферии'
        verbose_name_plural = 'Типы периферии'


class ComputerConfiguration(NamedEntity):
    '''
    Конфигурация (сборка) компьютера.
    '''
    class Meta:
        verbose_name = 'Конфигурация (сборка) компьютера'
        verbose_name_plural = 'Конфигурации (сборки) компьютеров'

    processor = models.CharField(max_length=50, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    motherboard = models.CharField(max_length=50, verbose_name='Материнская плата')
    drives = models.TextField(verbose_name='Накопители')
    power_supply = models.CharField(max_length=50, verbose_name='Блок питания')


class Peripheral(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Периферийное устройство (мышь, клавиатура).
    '''
    class Meta:
        verbose_name = 'Периферия'
        verbose_name_plural = 'Периферия'

    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип периферии')


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Сетевое обородувание (роутеры, коммутаторы).
    '''
    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Копьютер.
    '''
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'

    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Монитор.
    '''
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    МФУ, принтер
    '''
    class Meta:
        verbose_name = 'МФУ'
        verbose_name_plural = 'МФУ'


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    ИБП (источник бесперебойного питания)
    '''
    class Meta:
        verbose_name = 'ИБП'
        verbose_name_plural = 'ИБП'


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Метео/гидро/агро оборудование
    '''
    class Meta:
        verbose_name = 'Прибор (гидро / метео / агро)'
        verbose_name_plural = 'Приборы (гидро / метео / агро)'


class Server(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Сервер.
    '''
    class Meta:
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'

    purpose = models.TextField(default='', verbose_name='Назначение')


class Cartridge(NamedEntity, TechnicalConditionEntity):
    '''
    Картридж.
    '''
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджы'

    mfp = models.ForeignKey(MFP, on_delete=models.CASCADE, verbose_name='МФУ', null=True, blank=True)

    def __str__(self):
        match self.technical_condition:
            case self.TechnicalCondition.READY_TO_USE:
                return f'{self.name} готов к установке.'
            case self.TechnicalCondition.IN_WORK:
                return f'{self.name} установлен в {self.mfp}.'
            case self.TechnicalCondition.DISABLED:
                return f'{self.name} снят по причине {self.disabling_reason}.'
            case self.TechnicalCondition.REPAIRING:
                return f'{self.name} на ремонте/обслуживании по причине {self.disabling_reason}.'


class Request(WorksitePlaced):
    '''
    Запросы на ремонт / замену
    '''
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    class RequestStatus(models.IntegerChoices):
        CREATED = 0, 'Создан'
        IN_WORK = 1, 'В работе'
        COMPLETED = 2, 'Выполнен'

    description = models.TextField(default='', verbose_name='Описание запроса')
    status = models.IntegerField(choices=RequestStatus, verbose_name='Статус запроса', default=RequestStatus.CREATED)
    created_at = models.DateTimeField(null=True, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, verbose_name='Выполнен')
