from django import forms

from .models import Cartridge


class CartridgeForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = ['name', 'number', 'technical_condition', 'mfp', 'disabling_reason', 'refills']
        widgets = {
            'disabling_reason': forms.Textarea(attrs={'cols': 80, 'rows': 1})
        }


CartridgeAddFormSet = forms.modelformset_factory(
    Cartridge,
    form=CartridgeForm,
    fields=['name', 'number', 'technical_condition', 'mfp', 'disabling_reason', 'refills'],
    extra=1,
)

CartridgeEditFormSet = forms.modelformset_factory(
    Cartridge,
    form=CartridgeForm,
    fields=['name', 'number', 'technical_condition', 'mfp', 'disabling_reason', 'refills'],
    extra=0,
)
