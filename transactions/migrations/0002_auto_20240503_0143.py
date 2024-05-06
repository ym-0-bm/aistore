# Generated by Django 3.0.7 on 2024-05-03 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleachat',
            name='prixunitaire',
        ),
        migrations.AddField(
            model_name='facturevente',
            name='genre',
            field=models.CharField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme', max_length=7),
            preserve_default=False,
        ),
    ]
