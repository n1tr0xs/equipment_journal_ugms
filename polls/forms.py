from django.forms import ModelForm, modelformset_factory

from .models import Cartridge


class CartridgeAddForm(ModelForm):
    class Meta:
        model = Cartridge
        fields = ['name', 'number']


CartridgeFormSet = modelformset_factory(
    Cartridge, fields='__all__', extra=1,
)
