import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from .models import TotalEnergie, Dynef
def import_total_energie_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for elem in root:
        prix = float(elem.find('PRIX').text)
        date_debut = datetime.strptime(elem.find('DATEDEBUT').text, '%Y-%m-%d').date()
        date_fin = datetime.strptime(elem.find('DATEFIN').text, '%Y-%m-%d').date()
        total_energie = TotalEnergie(prix=prix, date_debut=date_debut, date_fin=date_fin)
        total_energie.save()

def import_dynef_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dynef = Dynef()
            dynef.prix = float(row['prix'])
            dynef.type = row['type']
            dynef.marge = float(row['marge'])
            dynef.date_debut = datetime.strptime(row['Date Debut'], '%Y-%m-%d').date()
            dynef.duree = int(row['durre'])
            dynef.date_fin = datetime.strptime(row['Date Fin'], '%Y-%m-%d').date()
            dynef = Dynef(prix=prix, date_debut=date_debut, date_fin=date_fin)
            dynef.save()


