from django.db import models


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    nom_category = models.CharField(max_length=70, unique=True)


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=30, unique=True)
    quantite = models.IntegerField(default=1)
    prix = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categorystock')

    def __str__(self):
        return self.nom
