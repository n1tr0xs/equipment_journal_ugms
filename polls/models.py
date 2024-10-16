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


class Peripheral(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Периферийное устройство (мышь, клавиатура).
    '''
    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип переферии')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Сетевое обородувание (роутеры, коммутаторы).
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Копьютер.
    '''
    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Монитор.
    '''
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    МФУ, принтер
    '''
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    ИБП (источник бесперебойного питания)
    '''
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Метео/гидро/агро оборудование
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


class Server(NamedEntity, Inventoried, TechnicalConditionEntity):
    '''
    Сервер.
    '''
    purpose = models.TextField(default='', verbose_name='Назначение')

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура', null=True, blank=True)


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


class Request(models.Model):
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

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место', null=True, blank=True)
