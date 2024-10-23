from django import forms

from .models import Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request


class StructureForm(forms.ModelForm):
    class Meta:
        model = Structure
        fields = ['name', 'physical_place']
        widgets = {
            'physical_place': forms.Textarea(attrs={'rows': 1}),
        }


StructureFormSet = forms.modelformset_factory(
    Structure,
    form=StructureForm,
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'structure']
        widgets = {}


PostFormSet = forms.modelformset_factory(
    Post,
    form=PostForm,
)


class WorksiteForm(forms.ModelForm):
    class Meta:
        model = Worksite
        fields = ['name', 'post']
        widgets = {}


WorksiteFormSet = forms.modelformset_factory(
    Worksite,
    form=WorksiteForm,
)


class PeripheralTypeForm(forms.ModelForm):
    class Meta:
        model = PeripheralType
        fields = ['name']
        widgets = {}


PeripheralTypeFormSet = forms.modelformset_factory(
    PeripheralType,
    form=PeripheralTypeForm,
)


class ComputerConfigurationForm(forms.ModelForm):
    class Meta:
        model = ComputerConfiguration
        fields = ['name', 'processor', 'ram', 'motherboard', 'drives', 'power_supply']
        widgets = {
            'drives': forms.Textarea(attrs={'rows': 1}),
        }


ComputerConfigurationFormSet = forms.modelformset_factory(
    ComputerConfiguration,
    form=ComputerConfigurationForm,
)


class PeripheralForm(forms.ModelForm):
    class Meta:
        model = Peripheral
        fields = ['name', 'peripheral_type', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'worksite']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


PeripheralFormSet = forms.modelformset_factory(
    Peripheral,
    form=PeripheralForm,
)


class NetworkEquipmentForm(forms.ModelForm):
    class Meta:
        model = NetworkEquipment
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'structure', 'ip_address']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


NetworkEquipmentFormSet = forms.modelformset_factory(
    NetworkEquipment,
    form=NetworkEquipmentForm,
)


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ['name', 'configuration', 'comment', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'worksite', 'ip_address']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


ComputerFormSet = forms.modelformset_factory(
    Computer,
    form=ComputerForm,
)


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'worksite']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


MonitorFormSet = forms.modelformset_factory(
    Monitor,
    form=MonitorForm,
)


class MFPForm(forms.ModelForm):
    class Meta:
        model = MFP
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'worksite']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


MFPFormSet = forms.modelformset_factory(
    MFP,
    form=MFPForm,
)


class UPSForm(forms.ModelForm):
    class Meta:
        model = UPS
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'worksite']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


UPSFormSet = forms.modelformset_factory(
    UPS,
    form=UPSForm,
)


class MeteoUnitForm(forms.ModelForm):
    class Meta:
        model = MeteoUnit
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'structure', 'verification_date']
        widgets = {'disabling_reason': forms.Textarea(attrs={'rows': 1}), }


MeteoUnitFormSet = forms.modelformset_factory(
    MeteoUnit,
    form=MeteoUnitForm,
)


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'inventory_number', 'serial_number', 'technical_condition', 'disabling_reason', 'structure', 'ip_address', 'purpose']
        widgets = {
            'disabling_reason': forms.Textarea(attrs={'rows': 1}),
            'purpose': forms.Textarea(attrs={'rows': 1}),
        }


ServerFormSet = forms.modelformset_factory(
    Server,
    form=ServerForm,
)


class CartridgeForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = ['name', 'number', 'technical_condition', 'mfp', 'disabling_reason', 'refills']
        widgets = {
            'disabling_reason': forms.Textarea(attrs={'rows': 1}),
        }


CartridgeFormSet = forms.modelformset_factory(
    Cartridge,
    form=CartridgeForm,
)


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['description', 'worksite', 'status', 'created_at', 'completed_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }


RequestFormSet = forms.modelformset_factory(
    Request,
    form=RequestForm,
)


class RequestToDoForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['description', 'worksite', 'status', 'created_at', 'completed_at']
        widgets = {
            'worksite': forms.Select(attrs={'readonly': True}),
            'description': forms.Textarea(attrs={'rows': 1}),
            'created_at': forms.DateTimeInput(attrs={'readonly': True}),
            'completed_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


RequestToDoFormSet = forms.modelformset_factory(
    Request,
    form=RequestToDoForm,
)
