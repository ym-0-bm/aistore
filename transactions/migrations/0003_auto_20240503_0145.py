# Generated by Django 3.0.7 on 2024-05-03 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20240503_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlevente',
            name='prixunitaire',
        ),
        migrations.AddField(
            model_name='articleachat',
            name='prixunitaire',
            field=models.IntegerField(default=1),
        ),
    ]