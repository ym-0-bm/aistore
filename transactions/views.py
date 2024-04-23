from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    FactureAchat,
    Fournisseur,
    ArticleAchat,
    DetailsFactureAchat,
    FactureVente,
    ArticleVente,
    DetailsFactureVente
)
from .forms import (
    SelectFournisseurForm,
    ArticleAchatFormset,
    DetailsAchatForm,
    FournisseurForm,
    VenteForm,
    ArticleVenteFormset,
    DetailsVenteForm
)
from stock.models import Stock


class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "fournisseurs/liste_fournisseur.html"
    queryset = Fournisseur.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class FournisseurCreateView(SuccessMessageMixin, CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    success_url = '/transactions/fournisseurs'
    success_message = "Supplier has been created successfully"
    template_name = "fournisseurs/modif_fournisseur.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Fournisseur'
        context["savebtn"] = 'Ajouter Fournisseur'
        return context


class FournisseurUpdateView(SuccessMessageMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    success_url = '/transactions/fournisseurs'
    success_message = "Detail fournisseur a été ajouté avec succès"
    template_name = "fournisseurs/modif_fournisseur.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Modifier Fournisseur'
        context["savebtn"] = 'Enregistrer Modification'
        context["delbtn"] = 'Supprimer Fournisseur'
        return context


class FournisseurDeleteView(View):
    template_name = "fournisseurs/sup_fournisseur.html"
    success_message = "Fournisseur a été supprimé avec succès"

    def get(self, request, id):
        fournisseur = get_object_or_404(Fournisseur, id=id)
        return render(request, self.template_name, {'object': fournisseur})

    def post(self, request, pk):
        fournisseur = get_object_or_404(Fournisseur, id=id)
        fournisseur.is_deleted = True
        fournisseur.save()
        messages.success(request, self.success_message)
        return redirect('fournisseurs-list')


class FournisseurView(View):
    def get(self, request, name):
        fournisseurobj = get_object_or_404(Fournisseur, name=name)
        facture_list = FactureAchat.objects.filter(fournisseur=fournisseurobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(facture_list, 10)
        try:
            factures = paginator.page(page)
        except PageNotAnInteger:
            factures = paginator.page(1)
        except EmptyPage:
            factures = paginator.page(paginator.num_pages)
        context = {
            'fournisseur': fournisseurobj,
            'factures': factures
        }
        return render(request, 'fournisseurs/fournisseur.html', context)


class AchatView(ListView):
    model = FactureAchat
    template_name = "achats/liste_achat.html"
    context_object_name = 'factures'
    ordering = ['-date']
    paginate_by = 10


class FournisseurSelectView(View):
    form_class = SelectFournisseurForm
    template_name = 'achats/fournisseur_select.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            fournisseurid = request.POST.get("fournisseur")
            fournisseur = get_object_or_404(Fournisseur, id=fournisseurid)
            return redirect('new-purchase', fournisseur.id)
        return render(request, self.template_name, {'form': form})


class AchatCreateView(View):
    template_name = 'achats/new_achat.html'

    def get(self, request, id):
        formset = ArticleAchatFormset(request.GET or None)
        fournisseurobj = get_object_or_404(Fournisseur, id=id)
        context = {
            'formset': formset,
            'fournisseur': fournisseurobj,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        formset = ArticleAchatFormset(request.POST)
        fournisseurobj = get_object_or_404(Fournisseur, id=id)
        if formset.is_valid():
            factureobj = FactureAchat(
                fournisseur=fournisseurobj)
            factureobj.save()
            facturedetailsobj = DetailsFactureAchat(nofacture=factureobj)
            facturedetailsobj.save()
            for form in formset:
                articlefacture = form.save(commit=False)
                articlefacture.nofacture = factureobj
                stock = get_object_or_404(Stock, nom=articlefacture.stock.nom)
                articlefacture.montant = articlefacture.prixunitaire * articlefacture.quantite
                stock.quantite += articlefacture.quantite
                stock.save()
                articlefacture.save()
            messages.success(request, "Les articles achetés ont été enregistrés avec succès")
            return redirect('purchase-facture', nofacture=factureobj.nofacture)
        formset = ArticleAchatFormset(request.GET or None)
        context = {
            'formset': formset,
            'fournisseur': fournisseurobj
        }
        return render(request, self.template_name, context)


class SupAchatView(SuccessMessageMixin, DeleteView):
    model = FactureAchat
    template_name = "achats/sup_achat.html"
    success_url = '/transactions/achats'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        articles = ArticleAchat.objects.filter(nofacture=self.object.nofacture)
        for article in articles:
            stock = get_object_or_404(Stock, nom=article.stock.nom)
            if not stock.is_deleted:
                stock.quantite -= article.quantite
                stock.save()
        messages.success(self.request, "La facture d'achat a été supprimée avec succès")
        return super(SupAchatView, self).delete(*args, **kwargs)


class VenteView(ListView):
    model = FactureVente
    template_name = "ventes/liste_vente.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


class VenteCreateView(View):
    template_name = 'ventes/new_vente.html'

    def get(self, request):
        form = VenteForm(request.GET or None)
        formset = ArticleVenteFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = VenteForm(request.POST)
        formset = ArticleVenteFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            factureobj = form.save(commit=False)
            factureobj.save()
            detailsfactureobj = DetailsFactureVente(nofacture=nofacture)
            detailsfactureobj.save()
            for form in formset:
                articlefacture = form.save(commit=False)
                articlefacture.billno = factureobj
                stock = get_object_or_404(Stock, nom=articlefacture.stock.nom)
                articlefacture.montant = articlefacture.prixunitaire * articlefacture.quantite
                stock.quantite -= articlefacture.quantite
                stock.save()
                articlefacture.save()
            messages.success(request, "Les articles vendus ont été enregistrés avec succès")
            return redirect('sale-facture', nofacture=factureobj.nofacture)
        form = VenteForm(request.GET or None)
        formset = ArticleVenteFormset(request.GET or None)
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)


class SupVenteView(SuccessMessageMixin, DeleteView):
    model = FactureVente
    template_name = "ventes/sup_vente.html"
    success_url = '/transactions/ventes'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        articles = ArticleVente.objects.filter(nofacture=self.object.nofacture)
        for article in articles:
            stock = get_object_or_404(Stock, nom=article.stock.nom)
            if not stock.is_deleted:
                stock.quantite += article.quantity
                stock.save()
        messages.success(self.request, "La facture de vente a été supprimée avec succès")
        return super(SupVenteView, self).delete(*args, **kwargs)


class FactureAchatView(View):
    model = FactureAchat
    template_name = "facture/achat_facture.html"
    facture_base = "facture/facture_base.html"

    def get(self, request, nofacture):
        context = {
            'facture': FactureAchat.objects.get(nofacture=nofacture),
            'article': ArticleAchat.objects.filter(nofacture=nofacture),
            'detailsfacture': DetailsFactureAchat.objects.get(nofacture=nofacture),
            'facture_base': self.facture_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, nofacture):
        form = DetailsAchatForm(request.POST)
        if form.is_valid():
            detailsfactureobj = DetailsFactureAchat.objects.get(nofacture=nofacture)

            detailsfactureobj.eway = request.POST.get("eway")
            detailsfactureobj.veh = request.POST.get("veh")
            detailsfactureobj.destination = request.POST.get("destination")
            detailsfactureobj.po = request.POST.get("po")
            detailsfactureobj.cgst = request.POST.get("cgst")
            detailsfactureobj.sgst = request.POST.get("sgst")
            detailsfactureobj.igst = request.POST.get("igst")
            detailsfactureobj.cess = request.POST.get("cess")
            detailsfactureobj.tcs = request.POST.get("tcs")
            detailsfactureobj.total = request.POST.get("total")

            detailsfactureobj.save()
            messages.success(request, "Les détails de la facture ont été modifiés avec succès")
        context = {
            'facture': FactureAchat.objects.get(nofacture=nofacture),
            'article': ArticleAchat.objects.filter(nofacture=nofacture),
            'detailsfacture': DetailsFactureAchat.objects.get(nofacture=nofacture),
            'facture_base': self.facture_base,
        }
        return render(request, self.template_name, context)


class FactureVenteView(View):
    model = FactureVente
    template_name = "facture/vente_facture.html"
    facture_base = "facture/facture_base.html"

    def get(self, request, nofacture):
        context = {
            'facture': FactureVente.objects.get(nofacture=nofacture),
            'article': ArticleVente.objects.filter(nofacture=nofacture),
            'detailsfacture': DetailsFactureVente.objects.get(nofacture=nofacture),
            'facture_base': self.facture_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, nofacture):
        form = DetailsVenteForm(request.POST)
        if form.is_valid():
            detailsfactureobj = DetailsFactureVente.objects.get(nofacture=nofacture)

            detailsfactureobj.eway = request.POST.get("eway")
            detailsfactureobj.veh = request.POST.get("veh")
            detailsfactureobj.destination = request.POST.get("destination")
            detailsfactureobj.po = request.POST.get("po")
            detailsfactureobj.cgst = request.POST.get("cgst")
            detailsfactureobj.sgst = request.POST.get("sgst")
            detailsfactureobj.igst = request.POST.get("igst")
            detailsfactureobj.cess = request.POST.get("cess")
            detailsfactureobj.tcs = request.POST.get("tcs")
            detailsfactureobj.total = request.POST.get("total")

            detailsfactureobj.save()
            messages.success(request, "Les détails de la facture ont été modifiés avec succès")
        context = {
            'facture': FactureVente.objects.get(nofacture=nofacture),
            'article': ArticleVente.objects.filter(nofacture=nofacture),
            'detailsfacture': DetailsFactureVente.objects.get(nofacture=nofacture),
            'facture_base': self.facture_base,
        }
        return render(request, self.template_name, context)
