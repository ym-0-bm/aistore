from django.db import models


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=30, unique=True)
    quantite = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
