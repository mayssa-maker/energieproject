import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from .models import TotalEnergie, Dyneff
import codecs
def import_total_energie_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for elem in root:
        prix = float(elem.find('prix').text.replace(',', '.'))
        date_debut = datetime.strptime(elem.find('DateDebut').text, '%d/%m/%Y').date()
        date_fin = datetime.strptime(elem.find('DateFin').text, '%d/%m/%Y').date()
        total_energie = TotalEnergie(prix=prix, date_debut=date_debut, date_fin=date_fin)
        total_energie.save()

def import_dynef_from_csv(file):
  
     reader=csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
     for row in reader:
        dynef = Dyneff()
        dynef.prix = float(row['prix'].replace(',', '.'))
        dynef.date_debut = datetime.strptime(row['Date Debut'], '%d/%m/%Y').date()
        dynef.date_fin = datetime.strptime(row['Date Fin'], '%d/%m/%Y').date()
        dynef.save()             
              
  



