from rest_framework import serializers
from .models import Compte
from rest_framework import serializers
from .models import Societe
from .models import Compteur,Dynef
class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ['id', 'email', 'nom', 'prenom', 'password', 'societe']
        read_only_fields = ['id']


class SocieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Societe
        fields = ['id', 'siret', 'raison_sociale']


class CompteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compteur
        fields = ['num_compteur', 'type_energie', 'consommation', 'societe']
        read_only_fields = ['societe']

class DynefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dynef
        fields =['prix', 'date_debut','date_fin']
