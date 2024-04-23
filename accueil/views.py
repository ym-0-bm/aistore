from django.shortcuts import render
from django.views.generic import View, TemplateView
from stock.models import Stock
from transactions.models import FactureVente, FactureAchat


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantite')
        for item in stockqueryset:
            labels.append(item.nom)
            data.append(item.quantite)
        ventes = FactureVente.objects.order_by('-date')[:3]
        achats = FactureAchat.objects.order_by('-date')[:3]
        context = {
            'labels': labels,
            'data': data,
            'ventes': ventes,
            'achats': achats
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "about.html"
