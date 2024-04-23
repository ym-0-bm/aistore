from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseurs-list'),
    path('fournisseur/new', views.FournisseurCreateView.as_view(), name='new-fournisseurs'),
    path('fournisseurs/<id>/modif', views.FournisseurUpdateView.as_view(), name='modif-fournisseurs'),
    path('fournisseurs/<id>/sup', views.FournisseurDeleteView.as_view(), name='sup-fournisseurs'),
    path('fournisseurs/<nom>', views.FournisseurView.as_view(), name='fournisseurs'),

    path('achats/', views.AchatView.as_view(), name='achats-list'),
    path('achats/new', views.FournisseurSelectView.as_view(), name='select-fournisseur'),
    path('achats/new/<id>', views.AchatCreateView.as_view(), name='new-achats'),
    path('achats/<id>/sup', views.SupAchatView.as_view(), name='sup-achats'),
    
    path('ventes/', views.VenteView.as_view(), name='ventes-list'),
    path('ventes/new', views.VenteCreateView.as_view(), name='new-ventes'),
    path('ventes/<id>/sup', views.SupVenteView.as_view(), name='sup-ventes'),

    path("achats/<nofacture>", views.FactureAchatView.as_view(), name="achat-facture"),
    path("ventes/<nofacture>", views.FactureVenteView.as_view(), name="ventes-facture"),
]