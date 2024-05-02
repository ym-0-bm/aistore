from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView,
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock, Category
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'stock.html'
    paginate_by = 10


class StockCreateView(SuccessMessageMixin,
                      CreateView):
    model = Stock
    form_class = StockForm
    template_name = "modif_stock.html"
    success_url = '/stock'
    success_message = "Stock a été ajouté avec succès"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nouveau Stock'
        context["savebtn"] = 'Ajouter au Stock'
        return context


class StockUpdateView(SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "modif_stock.html"
    success_url = '/stock'
    success_message = "Stock a été mis à jour avec succès"

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Stock, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Modifier Stock'
        context["savebtn"] = 'Mise à jour Stock'
        context["delbtn"] = 'Supprimer Stock'
        return context


class StockDeleteView(View):
    template_name = "sup_stock.html"
    success_message = "Stock a été supprimé avec succès"

    def get(self, request, id):
        stock = get_object_or_404(Stock, id=id)
        return render(request, self.template_name, {'object': stock})

    def post(self, request, id):
        stock = get_object_or_404(Stock, id=id)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('stock')
