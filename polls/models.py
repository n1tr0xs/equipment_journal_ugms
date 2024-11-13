from django.utils import timezone
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

    ip_address = models.GenericIPAddressField(protocol='ipv4', unique=True, verbose_name='IP адрес')


class Inventoried(models.Model):
    class Meta:
        abstract = True

    inventory_number = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='Инвентарный номер')
    serial_number = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='Серийный номер')


class TechnicalCondition(models.IntegerChoices):
    READY_TO_USE = 0, 'Готов к установке'
    IN_WORK = 1, 'В работе'
    DISABLED = 2, 'Снят (нерабочий)'
    REPAIRING = 3, 'В ремонте'


class DeviceTypeChoices(models.IntegerChoices):
    PERIPHERAL = 0, 'Периферия'
    COMPUTER = 1, 'Комьютер'
    MFP = 2, 'МФУ'
    NETWORKEQUIPMENT = 3, 'Сетевое оборудование'
    MONITOR = 4, 'Монитор'
    UPS = 5, 'ИБП'
    METEOUNIT = 6, 'Прибор'
    SERVER = 7, 'Сервер'
    CARTRIDGE = 8, 'Картридж'


class ServiceHistory(models.Model):
    class Meta:
        verbose_name = 'История обслуживания'
        verbose_name_plural = 'История обслуживания'
    device_id = models.PositiveIntegerField()
    service_date_start = models.DateField(auto_now_add=True, verbose_name='Начало обслуживания', help_text='Начало обслуживания')
    service_date_end = models.DateField(null=True, verbose_name='Конец обслуживания', help_text='Конец обслуживания')
    description = models.TextField(verbose_name='Описание', help_text='Описание обслуживания')
    device_type = models.IntegerField(choices=DeviceTypeChoices, null=True, verbose_name='Тип устройства')

    def end(self):
        self.service_date_end = timezone.now()
        self.save()

    def get_device(self):
        return self.get_device_table().objects.get(pk=self.device_id)

    def get_device_table(self):
        match self.device_type:
            case DeviceTypeChoices.PERIPHERAL:
                return Peripheral
            case DeviceTypeChoices.COMPUTER:
                return Computer
            case DeviceTypeChoices.MFP:
                return MFP
            case DeviceTypeChoices.NETWORKEQUIPMENT:
                return NetworkEquipment
            case DeviceTypeChoices.MONITOR:
                return Monitor
            case DeviceTypeChoices.UPS:
                return UPS
            case DeviceTypeChoices.METEOUNIT:
                return MeteoUnit
            case DeviceTypeChoices.SERVER:
                return Server
            case DeviceTypeChoices.CARTRIDGE:
                return Cartridge
        return None


class TechnicalConditionEntity(models.Model):
    class Meta:
        abstract = True

    technical_condition = models.IntegerField(choices=TechnicalCondition, default=TechnicalCondition.READY_TO_USE, verbose_name='Техническое состояние')
    disabling_reason = models.TextField(default='', blank=True, verbose_name='Причина снятия')
    device_type = models.IntegerField(choices=DeviceTypeChoices, null=True, verbose_name='Тип устройства')
    last_service = models.ForeignKey(ServiceHistory, on_delete=models.SET_NULL, null=True)

    def get_service_history(self):
        return ServiceHistory.objects.filter(device_type__exact=self.device_type).filter(device_id__exact=self.id)


class Structure(NamedEntity):
    class Meta:
        verbose_name = 'Отдел / подразделение'
        verbose_name_plural = 'Отделы / подразеления'

    short_name = models.CharField(max_length=15, null=True, blank=True, verbose_name='Сокращение')
    physical_place = models.TextField(verbose_name='Физическое расположение')

    def __str__(self):
        return f'{self.short_name}'


class StructurePlaced(models.Model):
    class Meta:
        abstract = True

    structure = models.ForeignKey(Structure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Отдел / подразделение')


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

    name = models.CharField(max_length=100, default='', verbose_name='ФИО')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Должность')

    def __str__(self):
        return f'{self.name}, {self.post}'


class WorksitePlaced(models.Model):
    class Meta:
        abstract = True

    worksite = models.ForeignKey(Worksite, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рабочее место')


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

    peripheral_type = models.ForeignKey(PeripheralType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип периферии')
    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.PERIPHERAL, verbose_name='Тип устройства')

    def __str__(self):
        return f'{self.name} установлена на {self.worksite}'


class NetworkEquipment(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.NETWORKEQUIPMENT, verbose_name='Тип устройства')

    def __str__(self):
        return f'{self.name} {self.ip_address}'


class Computer(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced, IPEntity):
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'

    comment = models.CharField(max_length=100, default='', blank=True, verbose_name='Комменарий')
    configuration = models.ForeignKey(ComputerConfiguration, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Конфигурация (сборка)')
    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.COMPUTER, verbose_name='Тип устройства')

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class Monitor(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.MONITOR, verbose_name='Тип устройства')

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class MFP(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'МФУ'
        verbose_name_plural = 'МФУ'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.MFP, verbose_name='Тип устройства')
    installed_cartridge = models.OneToOneField('Cartridge', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Картридж')

    def save(self, *args, triggered=False, **kwargs):
        super().save(*args, **kwargs)
        if triggered:
            return

        # change previous cartridge mfp to `Null`, state to `
        try:
            prev_cartridge = Cartridge.objects.get(current_mfp=self)
            prev_cartridge.current_mfp_id = None
            prev_cartridge.save(triggered=True)
        except Cartridge.DoesNotExist:
            pass
        # change selected cartridge mfp to self
        selected_cartridge = self.installed_cartridge
        try:
            selected_cartridge.current_mfp = self
            selected_cartridge.save(triggered=True)
        except AttributeError:
            pass

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class UPS(NamedEntity, Inventoried, TechnicalConditionEntity, WorksitePlaced):
    class Meta:
        verbose_name = 'ИБП'
        verbose_name_plural = 'ИБП'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.UPS, verbose_name='Тип устройства')

    def __str__(self):
        return f'{self.name}, {self.worksite}'


class MeteoUnit(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced):
    class Meta:
        verbose_name = 'Прибор (гидро / метео / агро)'
        verbose_name_plural = 'Приборы (гидро / метео / агро)'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.METEOUNIT, verbose_name='Тип устройства')
    verification_date = models.DateField(null=True, blank=True, verbose_name='Дата поверки', help_text='Дата в формате DD.MM.YYYY')

    def __str__(self):
        return f'{self.name}, {self.structure}'


class Server(NamedEntity, Inventoried, TechnicalConditionEntity, StructurePlaced, IPEntity):
    class Meta:
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'

    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.SERVER, verbose_name='Тип устройства')
    purpose = models.TextField(default='', blank=True, verbose_name='Назначение')

    def __str__(self):
        return f'{self.name} - {self.ip_address}'


class Cartridge(NamedEntity, TechnicalConditionEntity):
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'

    number = models.CharField(max_length=50, default='', blank=True, unique=True, verbose_name='Номер картриджа')
    refills = models.PositiveIntegerField(default=0, verbose_name='Количество заправок')
    current_mfp = models.OneToOneField(MFP, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='МФУ')
    device_type = models.IntegerField(choices=DeviceTypeChoices, default=DeviceTypeChoices.CARTRIDGE, verbose_name='Тип устройства')

    def save(self, *args, triggered=False, **kwargs):
        if (self.current_mfp_id):
            if (self.technical_condition in [TechnicalCondition.DISABLED, TechnicalCondition.READY_TO_USE, TechnicalCondition.REPAIRING]):
                self.technical_condition = TechnicalCondition.IN_WORK
        if (self.current_mfp_id is None):
            if (self.technical_condition == TechnicalCondition.IN_WORK):
                self.technical_condition = TechnicalCondition.DISABLED

        super().save(*args, **kwargs)

        if triggered:
            return

        try:
            prev_mfp = MFP.objects.get(installed_cartridge=self)
            prev_mfp.installed_cartridge = None
            prev_mfp.save(triggered=True)
        except MFP.DoesNotExist:
            pass

        selected_mfp = self.current_mfp
        try:
            selected_mfp.installed_cartridge = self
            selected_mfp.save(triggered=True)
        except AttributeError:
            pass

    def __str__(self):
        return f'{self.name} {self.number}, {self.current_mfp}'


class RequestStatus(models.IntegerChoices):
    CREATED = 0, 'Создан'
    IN_WORK = 1, 'В работе'
    COMPLETED = 2, 'Выполнен'


class Request(WorksitePlaced):
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    description = models.TextField(default='', verbose_name='Описание запроса')
    status = models.IntegerField(choices=RequestStatus, default=RequestStatus.CREATED, blank=True, verbose_name='Статус запроса')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Создан', help_text='Дата и время в формате DD.MM.YYYY hh:mm:ss')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Выполнен', help_text='Дата и время в формате DD.MM.YYYY hh:mm:ss')

    def get_absolute_url(self):
        return reverse('request-detail', kwargs={'pk': self.pk})
