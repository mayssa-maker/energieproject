from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompteSerializer
from .serializers import SocieteSerializer
from .serializers import DynefSerializer
from rest_framework import generics
from .models import Societe
from .models import Compte
from .models import Compteur
from .models import HistoriqueCalcul
from .models import TotalEnergie
from .models import Dynef
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .serializers import CompteurSerializer
from datetime import datetime
import os
from django.conf import settings
from .data_import import import_total_energie_from_xml, import_dynef_from_csv
import csv
import io

class CreerCompteView(generics.CreateAPIView,generics.ListAPIView):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

    def post(self, request):
        serializer = CompteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CreateSocieteView(generics.CreateAPIView,generics.ListAPIView):
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer

    def post(self, request, *args, **kwargs):
        # Check if the siret already exists in the database
        siret = request.data.get('siret')
        if Societe.objects.filter(siret=siret).exists():
            return Response({'error': 'This SIRET already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SocieteListByCompteView(generics.ListAPIView):
    serializer_class = SocieteSerializer

    def get_queryset(self):
        compte = get_object_or_404(Compte, id=self.kwargs['compte_id'])
        return Societe.objects.filter(compte=compte)
class SocieteRetrieveAPIView(RetrieveAPIView):
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer
    lookup_field = 'siret'



class AddCompteurView(generics.CreateAPIView,generics.ListAPIView):
    serializer_class = CompteurSerializer
    def get_queryset(self):
        return Compteur.objects.all()
    def post(self, request, siret):
        societe = get_object_or_404(Societe, siret=siret)
        serializer = CompteurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(societe=societe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompteurListView(generics.ListAPIView):
    serializer_class = CompteurSerializer

    def get_queryset(self):
        # Get the societe object based on the given siret in the URL
        societe = get_object_or_404(Societe, siret=self.kwargs['siret'])
        # Return a queryset of all the Compteurs related to the societe object
        return Compteur.objects.filter(societe=societe)

class CompteurListByCompte(generics.ListAPIView):
    serializer_class = CompteurSerializer

    def get_queryset(self):
        compte_id = self.kwargs['compte_id']
        queryset = Compteur.objects.filter(societe__compte=compte_id)
        return queryset
class PrixContratView(generics.ListAPIView):
   def get(self, request, *args, **kwargs):
        siret = kwargs.get('siret')
        num_compteur = kwargs.get('num_compteur')
        date_debut = datetime.strptime(kwargs.get('date_debut'), '%Y-%m-%d').date()
        date_fin = datetime.strptime(kwargs.get('date_fin'), '%Y-%m-%d').date()
        type_energie = kwargs.get('type_energie')

        # retrieve the relevant objects from the database
        compteur = get_object_or_404(Compteur, societe__siret=siret, num_compteur=num_compteur, type_energie=type_energie)
        if type_energie == 'Gaz':
            contrat = get_object_or_404(Dynef, date_debut__lte=date_debut, date_fin__gte=date_fin)
        elif type_energie == 'ELEC':
            contrat = get_object_or_404(TotalEnergie, date_debut__lte=date_debut, date_fin__gte=date_fin)

        # perform the calculation
        prix_contrat = compteur.consommation * contrat.prix

        # store the calculation result in the database
        historique = HistoriqueCalcul.objects.create(dateToday=datetime.now().date(), result=prix_contrat)
        if type_energie == 'Gaz':
            historique.dynef = contrat
        elif type_energie == 'ELEC':
            historique.total_energie = contrat
        historique.save()

        return JsonResponse({'prix_contrat': prix_contrat})
from django.http import HttpResponse



class DynefImportView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Dynef.objects.all()
    serializer_class = DynefSerializer

    def post(self, request, format=None):
        file = '/home/maysa/Dyneff.csv'
        filename = file.name

        # Check if the uploaded file is a CSV file
        if not filename.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Decode the uploaded file and read the CSV data
        file_data = file.read().decode('utf-8')
        csv_data = csv.reader(file_data.splitlines(), delimiter=',')

        # Iterate over each row in the CSV data and save to database
        for row in csv_data:
            dynef = Dynef(
                prix=row['prix'],
                date_debut=row['Date Debut'],
                date_fin=row['Date Fin']
            )
            dynef.save()

        return Response({'message': 'CSV file imported successfully.'}, status=status.HTTP_201_CREATED)


