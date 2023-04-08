from django.db import models

class Compte(models.Model):
    email = models.EmailField(max_length=254)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    societe = models.ForeignKey('Societe', on_delete=models.CASCADE)
    historiquecalcul = models.ManyToManyField('HistoriqueCalcul')

class Societe(models.Model):
    siret = models.CharField(max_length=14)
    raison_sociale = models.CharField(max_length=50)

class HistoriqueCalcul(models.Model):
    dateToday = models.DateField()
    result = models.FloatField()
    total_energie = models.ForeignKey('TotalEnergie', on_delete=models.CASCADE)
    dynef = models.ForeignKey('Dynef', on_delete=models.CASCADE)

class Dynef(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()

class TotalEnergie(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()

class Compteur(models.Model):
    num_compteur = models.CharField(max_length=30)
    type_energie = models.CharField(max_length=30)
    consommation = models.FloatField()
    societe = models.ForeignKey('Societe', on_delete=models.CASCADE)

