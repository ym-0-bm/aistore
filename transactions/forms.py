from django import forms
from django.forms import formset_factory
from .models import (
    Fournisseur,
    FactureAchat,
    ArticleAchat,
    DetailsFactureAchat,
    FactureVente,
    ArticleVente,
    DetailsFactureVente
)
from stock.models import Stock


class SelectFournisseurForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fournisseur'].queryset = Fournisseur.objects.filter(is_deleted=False)
        self.fields['fournisseur'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = FactureAchat
        fields = ['fournisseur']


class ArticleAchatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantite'].widget.attrs.update(
            {'class': 'textinput form-control prixunitaire quantité', 'min': '0', 'required': 'true'})
        self.fields['prixunitaire'].widget.attrs.update(
            {'class': 'textinput form-control prixunitaire prix', 'min': '0', 'required': 'true'})

    class Meta:
        model = ArticleAchat
        fields = ['stock', 'quantite', 'prixunitaire']


ArticleAchatFormset = formset_factory(ArticleAchatForm, extra=1)


class DetailsAchatForm(forms.ModelForm):
    class Meta:
        model = DetailsFactureAchat
        fields = ['total']


class FournisseurForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class': 'textinput form-control', 'pattern': '[a-zA-Z]{1,50}',
                                                'title': 'Alphabets et espaces uniquement'})
        self.fields['telephone'].widget.attrs.update(
            {'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}',
             'title': 'Chiffres uniquement'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = Fournisseur
        fields = ['nom', 'telephone', 'adresse', 'email']     # , 'gstin'
        widgets = {
            'adresse': forms.TextInput(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '4'
                }
            )
        }


class VenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update(
            {'class': 'textinput form-control', 'pattern': '[a-zA-Z]{1,50}',
             'title': 'Alphabets et espaces uniquement',
             'required': 'true'})
        self.fields['telephone'].widget.attrs.update(
            {'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}',
             'title': 'chiffres uniquement',
             'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = FactureVente
        fields = ['nom', 'telephone', 'adresse', 'email']
        widgets = {
            'adresse': forms.TextInput(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '4'
                }
            )
        }


class ArticleVenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantite'].widget.attrs.update(
            {'class': 'textinput form-control setprice quantite', 'min': '0', 'required': 'true'})
        self.fields['prixunitaire'].widget.attrs.update(
            {'class': 'textinput form-control setprice prix', 'min': '0', 'required': 'true'})

    class Meta:
        model = ArticleVente
        fields = ['stock', 'quantite']


ArticleVenteFormset = formset_factory(ArticleVenteForm, extra=1)


class DetailsVenteForm(forms.ModelForm):
    class Meta:
        model = DetailsFactureVente
        fields = ['total']
