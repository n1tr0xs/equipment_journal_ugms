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
    physical_place = models.TextField(verbose_name='Физическое расположение')


class Post(NamedEntity):
    '''
    Должность работника.
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')


class Worksite(NamedEntity):
    '''
    Рабочее место.
    '''
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


class ComputerConfiguration(NamedEntity):
    '''
    Конфигурация (сборка) компьютера.
    '''
    processor = models.CharField(max_length=50, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    motherboard = models.CharField(max_length=50, verbose_name='Материнская плата')
    drives = models.TextField(verbose_name='Накопители')
    power_supply = models.CharField(max_length=50, verbose_name='Блок питания')


class Peripheral(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Периферийное устройство (мышь, клавиатура).
    '''
    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип переферии')


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Сетевое обородувание (роутеры, коммутаторы).
    '''


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Копьютер.
    '''
    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    Монитор.
    '''


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    МФУ, принтер
    '''


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    '''
    ИБП (источник бесперебойного питания)
    '''


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Метео/гидро/агро оборудование
    '''


class Server(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    '''
    Сервер.
    '''
    purpose = models.TextField(default='', verbose_name='Назначение')


class Cartridge(NamedEntity, TechnicalConditionEntity):
    '''
    Картридж.
    '''
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
    class RequestStatus(models.IntegerChoices):
        CREATED = 0, 'Создан'
        IN_WORK = 1, 'В работе'
        COMPLETED = 2, 'Выполнен'

    description = models.TextField(default='', verbose_name='Описание запроса')
    status = models.IntegerField(choices=RequestStatus, verbose_name='Статус запроса', default=RequestStatus.CREATED)
    created_at = models.DateTimeField(null=True, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, verbose_name='Выполнен')
