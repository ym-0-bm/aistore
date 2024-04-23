from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='stock'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<id>/modif', views.StockUpdateView.as_view(), name='modif-stock'),
    path('stock/<id>/sup', views.StockDeleteView.as_view(), name='sup-stock'),
]