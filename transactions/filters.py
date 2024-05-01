import django_filters
from .models import ArticleAchat, ArticleVente, Fournisseur


class AchatFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ArticleAchat
        fields = ['stock']


class VenteFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ArticleVente
        fields = ['stock']


class FournisseurFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Fournisseur
        fields = ['nom']
