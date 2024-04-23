from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='stock'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('<int:id>/modification', views.StockUpdateView.as_view(), name='modif-stock'),
    path('<int:id>/suppression', views.StockDeleteView.as_view(), name='sup-stock'),
]