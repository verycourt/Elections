from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
url = "https://presidentielle2017.conseil-constitutionnel.fr/les-parrainages/parrainages-par-candidat/"


def loadHTML(url):
    resultats = requests.get(url)
    return BeautifulSoup(resultats.text, 'html.parser')

def extractSponsoring(url):
    table = loadHTML(url).find("table")
    rows = table.findAll('tr')
    candOfInterest = ['ARTHAUD','MACRON','MELENCHON','LE PEN','HAMON','FILLON','DUPONT-AIGNAN','POUTOU','JUPPE', 'CHEMINADE']
    candidates = []
    for row in rows[1:] :
        currcand = {}
        name = row .findAll('td')[0].text.split(' ')[0]
        if name not in candOfInterest : continue
        currcand['Nom'] = name
        currcand['01 mars'] = row.findAll('td')[2].text
        currcand['03 mars'] = row.findAll('td')[3].text
        currcand['07 mars'] = row.findAll('td')[4].text
        currcand['10 mars'] = row.findAll('td')[5].text
        currcand['14 mars'] = row.findAll('td')[6].text
        currcand['18 mars'] = row.findAll('td')[7].text
        candidates.append(currcand)
    return candidates

dump = pd.DataFrame(extractSponsoring(url))
dump.set_index('Nom', inplace=True)
dump.to_json('/var/www/html/parrainages/parrainages.json', orient='split')

