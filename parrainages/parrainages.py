from bs4 import BeautifulSoup
import json
import requests
url = "https://presidentielle2017.conseil-constitutionnel.fr/les-parrainages/parrainages-par-candidat/"


def loadHTML(url):
    resultats = requests.get(url)
    return BeautifulSoup(resultats.text, 'html.parser')

def extractSponsoring(url):
    table = loadHTML(url).find("table")
    rows = table.findAll('tr')
    candOfInterest = ['MACRON','MELENCHON','LE PEN','HAMON','FILLON','DUPONT-AIGNAN','POUTOU']
    candidates = []
    for row in rows[1:] :
        currcand = {}
        name = row .findAll('td')[0].text.split(' ')[0]
        if name not in candOfInterest : continue
        currcand['Nom'] = name
        currcand['Nombre de parrainages'] =  row.findAll('td')[1].text
        currcand['01/03/2017'] =  row.findAll('td')[2].text
        currcand['03/03/2017'] =  row.findAll('td')[3].text
        currcand['07/03/2017'] =  row.findAll('td')[4].text
        currcand['10/03/2017'] =  row.findAll('td')[5].text
        currcand['14/03/2017'] =  row.findAll('td')[6].text
        currcand['18/03/2017'] =  row.findAll('td')[7].text
        candidates.append(currcand)
    return candidates
file = open('/var/www/html/parrainages/parrainages.json','w')
json.dump(extractSponsoring(url),file)
file.close()

