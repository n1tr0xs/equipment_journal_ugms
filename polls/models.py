from django.db import models

# Create your models here.


class NamedEntity(models.Model):
    name = models.CharField(max_length=100, default='', verbose_name='Название')

    def __str__(self):
        return f'Название: {self.name}'

    class Meta:
        abstract = True


class Inventoried(models.Model):
    '''
    Родительский класс для классов с инвентарным номером и серийным номером.
    '''
    inventory_number = models.CharField(max_length=100, default='', verbose_name='Инвентарный номер')
    serial_number = models.CharField(max_length=100, default='', verbose_name='Серийный номер')

    def __str__(self):
        return f'Название: {self.name}\nИнвентарный номер: {self.inventory_number}\nСерийный номер: {self.serial_number}'

    class Meta:
        abstract = True


class TechnicalCondition(NamedEntity):
    '''
    Техническое состояния оборудования.
    '''


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


class Peripheral(NamedEntity, Inventoried):
    '''
    Периферийное устройство (мышь, клавиатура).
    '''
    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE, verbose_name='Тип переферии')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')


class NetworkEquipment(NamedEntity, Inventoried):
    '''
    Сетевое обородувание (роутеры, коммутаторы).
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')


class Computer(NamedEntity, Inventoried):
    '''
    Копьютер.
    '''
    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE, verbose_name='Конфигурация (сборка)')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')


class Monitor(NamedEntity, Inventoried):
    '''
    Монитор.
    '''
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')


class MFP(NamedEntity, Inventoried):
    '''
    МФУ, принтер
    '''
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')


class UPS(NamedEntity, Inventoried):
    '''
    ИБП (источник бесперебойного питания)
    '''
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')


class MeteoUnit(NamedEntity, Inventoried):
    '''
    Метео/гидро/агро оборудование
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')


class Server(NamedEntity, Inventoried):
    '''
    Сервер.
    '''
    purpose = models.TextField(default='', verbose_name='')

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Структура')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')


class Cartridge(NamedEntity):
    '''
    Картридж.
    '''
    mfp = models.ForeignKey(MFP, on_delete=models.CASCADE, verbose_name='МФУ')
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE, verbose_name='Техническое состояние')


class Request(models.Model):
    '''
    Запросы на ремонт / замену
    '''
    description = models.TextField(default='', verbose_name='Описание запроса')
    created_at = models.DateTimeField(null=True, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, verbose_name='Выполнен')

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, verbose_name='Рабочее место')
