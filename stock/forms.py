from django import forms
from .models import Stock


class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantite'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Stock
        fields = ['nom', 'quantite']
