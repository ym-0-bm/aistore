from django.contrib import admin
from .models import (
    Fournisseur,
    FactureAchat,
    ArticleAchat,
    DetailsFactureAchat,
    FactureVente,
    ArticleVente,
    DetailsFactureVente
)

admin.site.register(Fournisseur)
admin.site.register(FactureAchat)
admin.site.register(ArticleAchat)
admin.site.register(DetailsFactureAchat)
admin.site.register(FactureVente)
admin.site.register(ArticleVente)
admin.site.register(DetailsFactureVente)