from django.db import models

# Create your models here.


class NamedEntity(models.Model):
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Inventoried(models.Model):
    '''
    Родительский класс для классов с инвентарным номером и серийным номером.
    '''
    inventory_number = models.CharField(max_length=100, default='')
    serial_number = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.name}\nИН: {self.inventory_number}\nS/N: {self.serial_number}'

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
    processor = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    motherboard = models.CharField(max_length=50)
    drives = models.TextField()
    power_supply = models.CharField(max_length=50)


class Structure(NamedEntity):
    '''
    Струтурное подразделения.
    '''
    physical_place = models.TextField()


class Post(NamedEntity):
    '''
    Должность работника.
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)


class Worksite(NamedEntity):
    '''
    Рабочее место.
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Peripheral(NamedEntity, Inventoried):
    '''
    Периферийное устройство (мышь, клавиатура).
    '''

    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)


class NetworkEquipment(NamedEntity, Inventoried):
    '''
    Сетевое обородувание (роутеры, коммутаторы).
    '''

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)


class Computer(NamedEntity, Inventoried):
    '''
    Копьютер.
    '''

    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)


class Monitor(NamedEntity, Inventoried):
    '''
    Монитор.
    '''

    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)


class MFP(NamedEntity, Inventoried):
    '''
    МФУ, принтер
    '''

    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)


class UPS(NamedEntity, Inventoried):
    '''
    ИБП (источник бесперебойного питания)
    '''

    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)


class MeteoUnit(NamedEntity, Inventoried):
    '''
    Метео/гидро/агро оборудование
    '''
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)


class Server(NamedEntity, Inventoried):
    '''
    Сервер.
    '''

    purpose = models.TextField()

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)


class Cartridge(NamedEntity):
    '''
    Картридж.
    '''
    mfp = models.ForeignKey(MFP, on_delete=models.CASCADE)
    technical_condition = models.ForeignKey(TechnicalCondition, on_delete=models.CASCADE)


class Request(models.Model):
    '''
    Запросы на ремонт / замену
    '''
    description = models.TextField(default='')
    created_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)
