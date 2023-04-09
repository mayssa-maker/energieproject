"""testEnergie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from energie.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptes/', CreerCompteView.as_view(), name='creer_compte'),
    path('societes/', CreateSocieteView.as_view(),name='create-societe'),
    path('comptes/<int:compte_id>/societes/', SocieteListByCompteView.as_view(), name='societe_list_by_compte'),
    path('societes/<str:siret>/', SocieteRetrieveAPIView.as_view(), name='societe_retrieve'),
    path('societe/<str:siret>/addcompteur/', AddCompteurView.as_view(), name='add-compteur'),
    path('societes/<str:siret>/compteurs/', CompteurListView.as_view(), name='compteur-list par societe'),
    path('comptes/<int:compte_id>/compteurs/', CompteurListByCompte.as_view(), name='compteur-list-by-compte'),
    path('prix_contrat/<str:siret>/<str:num_compteur>/<str:date_debut>/<str:date_fin>/<str:type_energie>/', PrixContratView.as_view(), name='prix_contrat'),
    path('import/', DynefImportView.as_view(), name='dynef_import'),
    path('importxml/',TotalEnergieImportView.as_view(),name='totalenergie_import'),
]