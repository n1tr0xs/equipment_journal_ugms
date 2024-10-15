from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(PeripheralType)
class PeripheralTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ComputerConfiguration)
class ComputerConfiguration(admin.ModelAdmin):
    list_display = ('id', 'name', 'processor', 'ram', 'motherboard', 'drives', 'power_supply')


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'physical_place')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure')


@admin.register(Worksite)
class WorksiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post')


@admin.register(Peripheral)
class PeripheralAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'peripheral_type', 'worksite', 'technical_condition', 'disabling_reason')


@admin.register(NetworkEquipment)
class NetworkEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'technical_condition', 'disabling_reason')


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'configuration', 'worksite', 'technical_condition', 'disabling_reason')


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'worksite', 'technical_condition', 'disabling_reason')


@admin.register(MFP)
class MFPAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'worksite', 'technical_condition', 'disabling_reason')


@admin.register(UPS)
class UPSAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'worksite', 'technical_condition', 'disabling_reason')


@admin.register(MeteoUnit)
class MeteoUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'technical_condition', 'disabling_reason')


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purpose', 'structure', 'technical_condition', 'disabling_reason')


@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mfp', 'technical_condition', 'disabling_reason')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'worksite', 'description', 'status', 'created_at', 'completed_at')
