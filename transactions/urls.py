from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseurs-list'),
    path('fournisseur/new', views.FournisseurCreateView.as_view(), name='new-fournisseur'),
    path('fournisseurs/<int:id>/modif', views.FournisseurUpdateView.as_view(), name='modif-fournisseur'),
    path('fournisseurs/<int:id>/sup', views.FournisseurDeleteView.as_view(), name='sup-fournisseur'),
    path('fournisseurs/<nom>', views.FournisseurView.as_view(), name='fournisseur'),

    path('achats/', views.AchatView.as_view(), name='achats-list'),
    path('achats/new', views.FournisseurSelectView.as_view(), name='select-fournisseur'),
    path('achats/new/<int:id>', views.AchatCreateView.as_view(), name='new-achats'),
    path('achats/<int:id>/sup', views.SupAchatView.as_view(), name='sup-achats'),
    
    path('ventes/', views.VenteView.as_view(), name='ventes-list'),
    path('ventes/new', views.VenteCreateView.as_view(), name='new-ventes'),
    path('ventes/<int:id>/sup', views.SupVenteView.as_view(), name='sup-ventes'),

    path("achats/<int:nofacture>", views.FactureAchatView.as_view(), name="achat-facture"),
    path("ventes/<int:nofacture>", views.FactureVenteView.as_view(), name="ventes-facture"),
]
