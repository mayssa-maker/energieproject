from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .data_import import *
from django.http import HttpResponse

#creation d'un compte
class CreerCompteView(generics.CreateAPIView,generics.ListAPIView):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

    def post(self, request):
        serializer = CompteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#ajout d'une societe
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
#Obtenir toutes les sociétés par compte
class SocieteListByCompteView(generics.ListAPIView):
    serializer_class = SocieteSerializer

    def get_queryset(self):
        compte = get_object_or_404(Compte, id=self.kwargs['compte_id'])
        return Societe.objects.filter(compte=compte)
#Obtenir une société par son Siret
class SocieteRetrieveAPIView(RetrieveAPIView):
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer
    lookup_field = 'siret'


#Ajouter un compteur à une société
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
#Obtenir la liste des compteurs par Société
class CompteurListView(generics.ListAPIView):
    serializer_class = CompteurSerializer

    def get_queryset(self):
        # Get the societe object based on the given siret in the URL
        societe = get_object_or_404(Societe, siret=self.kwargs['siret'])
        # Return a queryset of all the Compteurs related to the societe object
        return Compteur.objects.filter(societe=societe)
#Obtenir la liste des compteurs par compte
class CompteurListByCompte(generics.ListAPIView):
    serializer_class = CompteurSerializer

    def get_queryset(self):
        compte_id = self.kwargs['compte_id']
        queryset = Compteur.objects.filter(societe__compte=compte_id)
        return queryset
#Obtenir le prix d'un contrat d'énergie
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
class TotalEnergieImportView(generics.CreateAPIView):
    serializer_class = TotalEnergieSerializer

    def post(self, request, format=None):
        file_path = request.FILES['file']
        try:
            import_total_energie_from_xml(file_path)
            return Response({'success': 'File imported successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DynefImportView(APIView):
   
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if file is None:
            return Response({'error': 'No file was attached.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            import_dynef_from_csv(file)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': 'File imported successfully.'}, status=status.HTTP_201_CREATED)