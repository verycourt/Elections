import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

URL = "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l'%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2017#2016"

def loadHTML(URL):
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')
#for annee in range(2012, 2016):
tables = loadHTML(URL).findAll("table")

dfF = pd.DataFrame()

#Pour chaque table de wikipedia :
for table in tables :
    lignes = table.findAll("tr")

    #On récupère le nom de chaque colonne :
    colonnes = []
    for elem in lignes[0].findAll("th"):
        if elem.find("a") is None:
            colonnes.append(elem.text)
        else :
            colonnes.append(elem.find("a").text)
    #On crée un pandas dataframe pour stocker nos table :
    df = pd.DataFrame(columns = colonnes)
    #print(len(colonnes))

    nbRowspan = 0
    rowspan = []
    #our chaque ligne de notre table :

    for i, ligne in enumerate(lignes[2:]):
        line = []
        #lorsque certains éléments de notre tableau occupent plusieurs lignes

        if nbRowspan > 1 :
            for item in rowspan:
                line.append(item)
            nbRowspan-=1
        else :
            rowspan = []

        for elem in ligne.findAll("td"):
            if elem.has_attr("rowspan"):
                nbRowspan = int(elem["rowspan"])
                rowspan.append(elem.text)
            line.append(elem.text.replace("%", "").replace("-", "").replace("–",""))

        print(len(line))
        if len(line) > len(colonnes) -3 :
            df.loc[i] = line
        #print(df)

    print("end table")
    try:
        dfF = dfF.append(df)
    except Exception as e:
        print(df["Date"])


#print(dfF)
dfF.to_csv("C:\\Users\\Mohamed\\MS BGD\\fil_rouge_lepoint\\Sondages\BVA\\test.csv")
        #sondeur.append()


test = loadHTML(URL).findAll("table")[1].findAll("tr")[0].findAll("th")[0].text

plt.figure(1)

notCandidats = ["Date", "Sondeur", "Échantillon"]

#print(test)
for col in dfF.columns:
    if col not in notCandidats:
        dfF[col] = dfF[col].map(lambda x: x if isinstance(x, float) else np.nan)

x = range(len(dfF["Date"]))
plt.xticks(x, dfF["Date"])
#plt.plot(x,dfF["Nicolas Sarkozy"])
plt.plot(x,dfF["Marine Le Pen"], lw = 1)
plt.plot(x,dfF["Nicolas Sarkozy"], '-', lw=1)
