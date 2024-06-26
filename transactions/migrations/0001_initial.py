# Generated by Django 3.0.7 on 2024-05-02 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactureVente',
            fields=[
                ('nofacture', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=12)),
                ('adresse', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=12, unique=True)),
                ('adresse', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FactureAchat',
            fields=[
                ('nofacture', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achatfournisseur', to='transactions.Fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsFactureVente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(blank=True, null=True)),
                ('nofacture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailsfactureventeno', to='transactions.FactureVente')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsFactureAchat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(blank=True, default=1, null=True)),
                ('nofacture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodetailsfactureachat', to='transactions.FactureAchat')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleVente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=1)),
                ('prixunitaire', models.IntegerField(default=1)),
                ('montant', models.IntegerField(default=1)),
                ('nofacture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureventeno', to='transactions.FactureVente')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articlevente', to='stock.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleAchat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=1)),
                ('prixunitaire', models.IntegerField(default=1)),
                ('montant', models.IntegerField(default=1)),
                ('nofacture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nofactureachat', to='transactions.FactureAchat')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articleachat', to='stock.Stock')),
            ],
        ),
    ]
