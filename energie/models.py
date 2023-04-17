from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

class UserManager(BaseUserManager):
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

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)

class Compte(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    password = models.TextField(max_length=256)
    societe = models.ForeignKey('Societe', on_delete=models.CASCADE,null=True)
    historiquecalcul = models.ManyToManyField('HistoriqueCalcul')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

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

