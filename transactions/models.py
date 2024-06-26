from django.db import models
from stock.models import Stock


class Fournisseur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12, unique=True)
    adresse = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class FactureAchat(models.Model):
    nofacture = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='achatfournisseur')

    def __str__(self):
        return "No Facture: " + str(self.nofacture)

    def get_items_list(self):
        return ArticleAchat.objects.filter(nofacture=self)

    def get_total_price(self):
        articleachat = ArticleAchat.objects.filter(nofacture=self)
        total = 0
        for article in articleachat:
            total += article.montant
        return total


class ArticleAchat(models.Model):
    nofacture = models.ForeignKey(FactureAchat, on_delete=models.CASCADE, related_name='nofactureachat')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='articleachat')
    quantite = models.IntegerField(default=1)
    prixunitaire = models.IntegerField(default=1)
    montant = models.IntegerField(default=1)

    def __str__(self):
        return "No Facture: " + str(self.nofacture.nofacture) + ", Article = " + self.stock.nom


class DetailsFactureAchat(models.Model):
    nofacture = models.ForeignKey(FactureAchat, on_delete=models.CASCADE, related_name='nodetailsfactureachat')
    total = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return "No Facture: " + str(self.nofacture.nofacture)


class FactureVente(models.Model):
    HOMME = 'Homme'
    FEMME = 'Femme'

    GENRE_CHOICES = [
        (HOMME, 'Homme'),
        (FEMME, 'Femme'),
    ]

    nofacture = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=7, choices=GENRE_CHOICES)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    adresse = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return "No Facture: " + str(self.nofacture)

    def get_items_list(self):
        return ArticleVente.objects.filter(nofacture=self)

    def get_total_price(self):
        ArticlesVente = ArticleVente.objects.filter(nofacture=self)
        total = 0
        for article in ArticlesVente:
            total += article.montant
        return total


class ArticleVente(models.Model):
    nofacture = models.ForeignKey(FactureVente, on_delete=models.CASCADE, related_name='factureventeno')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='articlevente')
    quantite = models.IntegerField(default=1)
    montant = models.IntegerField(default=1)

    def __str__(self):
        return "No Facture: " + str(self.nofacture.nofacture) + ", Article = " + self.stock.nom


class DetailsFactureVente(models.Model):
    nofacture = models.ForeignKey(FactureVente, on_delete=models.CASCADE, related_name='detailsfactureventeno')
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "No Facture: " + str(self.nofacture.nofacture)
