from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CompteManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        compte = self.model(email=email, **extra_fields)
        # Encode password to bytes using UTF-8 encoding
        password = password.encode('utf-8')
        compte.set_password(password)
        compte.save(using=self._db)
        return compte


class Compte(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    password = models.TextField(max_length=256)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects =CompteManager()
    
    class Meta:
        db_table = "Compte"
    def __str__(self):
        return self.email

class Societe(models.Model):
    siret = models.CharField(max_length=14)
    raison_sociale = models.CharField(max_length=50)
    class Meta:
        db_table = "Societe"
class HistoriqueCalcul(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, related_name='historique_calcul',default=None)
    dateToday = models.DateField()
    result = models.FloatField()
    total_energie = models.ForeignKey('TotalEnergie', on_delete=models.CASCADE)
    dyneff = models.ForeignKey('Dyneff', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "HistoriqueCalcul"
class Dyneff(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    class Meta:
        db_table = "Dyneff"

class TotalEnergie(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    class Meta:
        db_table = "TotalEnergie"
class Compteur(models.Model):
    num_compteur = models.CharField(max_length=30)
    type_energie = models.CharField(max_length=30)
    consommation = models.FloatField()
    societe = models.ForeignKey('Societe', on_delete=models.CASCADE)
   
    class Meta:
        db_table = "Compteur"
