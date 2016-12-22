#!/usr/bin/python
# coding: utf8
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sys
import warnings
import dateparser

warnings.filterwarnings('ignore')

URL = "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l'%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2017#2016"
path = "data/"

def loadHTML(URL):
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')


def loadPandas(URL):
    tables = loadHTML(URL).findAll("table")

    dfF = pd.DataFrame()
    dfFs = pd.DataFrame()

    #Pour chaque table de wikipedia :
    for table in tables :
        lignes = table.findAll("tr")

        #On récupère le nom de chaque colonne :
        colonnes = []
        for elem in lignes[0].findAll("th"):
            if elem.find("a") is None :
                colonnes.append(elem.text)
            else :
                if(elem.find("a").text != ""):
                    colonnes.append(elem.find("a").text)
        if len(colonnes) < 7:
            for elem in lignes[2].findAll("th"):
                a=3
                colonnes.append(elem.text)

        #On crée un pandas dataframe pour stocker nos table :
        df = pd.DataFrame(columns = colonnes)

        #print(len(colonnes))

        nbRowspan = 0
        rowspan = []
        rowspanMil = []

        #our chaque ligne de notre table :
        for j,ligne in enumerate(lignes[2:]):
            line = list(np.zeros(len(colonnes)))
            line = ["/" for item in line]

            #lorsque certains éléments de notre tableau occupent plusieurs lignes
            for i,item in enumerate(rowspanMil):
                if item[0] > 1 :
                    line[item[1]] = item[2]
                    item[0] -= 1

            for i,elem in enumerate(ligne.findAll("td")):
                while line[i] != "/":
                    i+=1

                if elem.has_attr("rowspan"):
                    nbRowspan = int(elem["rowspan"])
                    if nbRowspan >1:
                        try :
                            rowspanMil.append([nbRowspan, i, float(elem.text.replace("%", "").replace(",",".").replace("<",""))])
                        except Exception as e :
                            rowspanMil.append([nbRowspan, i, (elem.text.replace("%", "").replace(",",".").replace("<",""))])
                try:
                    line[i] = (float(elem.text.replace("%", "").replace(",",".").replace("<","")))
                except Exception as e :
                    line[i] = (elem.text.replace("%", "").replace(",",".").replace("<",""))

            if len(line) > len(colonnes) - 3 :
                df.loc[j] = line
            #print(df)

        #2ème tour :
        if len(colonnes) < 7  :
            dfFs = dfFs.append(df)
        #1er tour :
        else :
            dfF = dfF.append(df)

    return (dfF, dfFs)

dfF, dfFs = loadPandas(URL)


#######################################################################
########################### 1er tour ##################################
#######################################################################

dfF = dfF.replace(to_replace=["-", "–"], value=" ")

notCandidats = [u"Date", u"Sondeur", u"Échantillon"]

anciensCandidats = [u"Alain Juppé", u"Bruno Le Maire", u"Jean-François Copé", u"Nicolas Sarkozy", u"Éva Joly"]

for col in dfF.columns:
    if col not in notCandidats:
        dfF[col] = dfF[col].map(lambda x: x if isinstance(x, float) else np.nan)


print(dfF.columns)
print(anciensCandidats)

dfF2 = dfF
for col in anciensCandidats:
    dfF2 = dfF2[dfF2[col].isnull()]
    dfF2 = dfF2.drop(col, axis=1)

#print(dfF)
dfF3 = dfF2.groupby(["Date"]).mean().reset_index()


dfF3["Date"] = dfF3["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[-3:]))
dfF3["Date"] = dfF3["Date"].map(lambda x : dateparser.parse(x).date())
dfF3 = dfF3.sort_values('Date', ascending=1)

def dateToString(date):
    if len(str(date.month))==1:
        month = "0"+str(date.month)
    else :
        month = str(date.month)

    if len(str(date.day))==1:
        day = "0"+str(date.day)
    else :
        day = str(date.day)
    return str(date.year)+month+day

dfF3 = dfF3.round(2)
dfF4 = dfF3


dfF4["date"] = dfF3["Date"].map(lambda x: dateToString(x))
dfF4 = dfF4.drop("Date", axis=1)

dfF4 = dfF4.set_index("date")
dfF4 = dfF4.dropna(axis=0, how='all')
dfF4 = dfF4.dropna(axis=1, how='all')


dfF4.to_csv(path+"sondages1er.csv", sep="\t", encoding='utf-8')

print(dfF4.head())

dfF4.to_csv(path+"sondages1er.csv", sep="\t", encoding='utf-8')

dfF4.to_csv(path+"data.tsv", sep="\t", encoding='utf-8')

#print(dfF3[["Manuel Valls", "Date"]])

#######################################################################
########################### 2nd tour ##################################
#######################################################################


dfFs2 = dfFs
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x if len(x)>5 else np.nan)
dfFs2 = dfFs2[dfFs2["Date"].notnull()]
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x.replace(u"-", " ").replace(u"–", " "))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[2:]))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : dateparser.parse(x).date())
dfFs2 = dfFs2.sort_values('Date', ascending=1)

notCandidats = [u"Date", u"Sondeur", u"Échantillon"]

def dateToString2(date):
    if len(str(date.month))==1:
        month = "0"+str(date.month)
    else :
        month = str(date.month)

    if len(str(date.day))==1:
        day = "0"+str(date.day)
    else :
        day = str(date.day)
    return day+"/"+month+"/"+str(date.year)


def getDuel(df, nom1, nom2):
    return df[[nom1, nom2, "date", "Abstention, blanc ou nul"]].set_index("date").dropna(axis=0, how='any')

for col in dfFs2.columns:
    if col not in notCandidats:
        dfFs2[col] = dfFs2[col].map(lambda x: x if isinstance(x, float) else np.nan)
        if col != "Abstention, blanc ou nul":
            dfFs2[col] = dfFs2[col]*(100-dfFs2["Abstention, blanc ou nul"])/100

dfFs2["date"] = dfFs2["Date"].map(lambda x: dateToString2(x))
dfFs2 = dfFs2.drop("Date", axis=1)


getDuel(dfFs2, u"Marine Le Pen", u"François Fillon").to_csv(path+"mlpVSff.tsv", sep="\t", encoding="utf-8")
getDuel(dfFs2, u"Marine Le Pen", u"Manuel Valls").to_csv(path+"mlpVSmv.tsv", sep="\t", encoding='utf-8')
getDuel(dfFs2, u"Marine Le Pen", u"Emmanuel Macron").to_csv(path+"mlpVSem.tsv", sep="\t", encoding='utf-8')

dfFs2.to_csv(path+"sondages2e.csv", encoding='utf-8')
print("Done")
