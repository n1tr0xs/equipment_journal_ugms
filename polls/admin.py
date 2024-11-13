from django.contrib import admin

from .models import *


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'physical_place']
    list_filter = []
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'structure']
    list_filter = []
    search_fields = ['name']


@admin.register(Worksite)
class WorksiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'post']
    list_filter = []
    search_fields = ['name']


@admin.register(PeripheralType)
class PeripheralTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = []
    search_fields = ['name']


@admin.register(ComputerConfiguration)
class ComputerConfiguration(admin.ModelAdmin):
    list_display = ['id', 'name', 'processor', 'ram', 'motherboard', 'drives', 'power_supply']
    list_filter = []
    search_fields = ['name']


@admin.register(Peripheral)
class PeripheralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'peripheral_type', 'worksite', 'technical_condition', 'disabling_reason', 'inventory_number', 'serial_number']
    list_filter = ['peripheral_type', 'worksite', 'technical_condition']
    search_fields = ['name']


@admin.register(NetworkEquipment)
class NetworkEquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'structure', 'technical_condition', 'disabling_reason', 'ip_address', 'inventory_number', 'serial_number']
    list_filter = ['structure', 'technical_condition']
    search_fields = ['name']


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'configuration', 'worksite', 'technical_condition', 'disabling_reason', 'inventory_number', 'serial_number']
    list_filter = ['configuration', 'worksite', 'technical_condition']
    search_fields = ['name']


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'worksite', 'technical_condition', 'disabling_reason', 'inventory_number', 'serial_number']
    list_filter = ['worksite', 'technical_condition']
    search_fields = ['name']


@admin.register(MFP)
class MFPAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'worksite', 'technical_condition', 'disabling_reason', 'inventory_number', 'serial_number']
    list_filter = ['worksite', 'technical_condition']
    search_fields = ['name']


@admin.register(UPS)
class UPSAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'worksite', 'technical_condition', 'disabling_reason', 'inventory_number', 'serial_number']
    list_filter = ['worksite', 'technical_condition']
    search_fields = ['name']


@admin.register(MeteoUnit)
class MeteoUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'structure', 'technical_condition', 'disabling_reason', 'verification_date', 'inventory_number', 'serial_number']
    list_filter = ['structure', 'technical_condition']
    search_fields = ['name']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'purpose', 'structure', 'technical_condition', 'disabling_reason', 'ip_address', 'inventory_number', 'serial_number']
    list_filter = ['structure', 'technical_condition']
    search_fields = ['name', 'purpose']


@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number', 'mfp', 'technical_condition', 'disabling_reason', 'refills']
    list_filter = ['technical_condition', 'refills']
    search_fields = ['name']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'worksite', 'description', 'status', 'created_at', 'completed_at']
    list_filter = ['worksite', 'status', 'created_at', 'completed_at']
    search_fields = ['description']


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'device_id', 'device_type', 'service_date_start', 'service_date_end', 'description']
    list_filter = ['device_type', 'service_date_start', 'service_date_end']
