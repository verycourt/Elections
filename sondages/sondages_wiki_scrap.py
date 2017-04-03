#!/usr/bin/python
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import warnings
import dateparser
import datetime
import time
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.1f')



warnings.filterwarnings('ignore')

URL = "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l'%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2017#2016"
path1 = "/var/www/html/1ertour/"
path2 = "/var/www/html/2ndtour/"

'''dicoTableMois = {4:"Janvier 2016", 5:"Février 2016", 6:"Mars 2016", 7:"Avril 2016", 8:"Mai 2016", 9:"Juin 2016",\
                 10:"Juillet 2016", 11:"Septembre 2016", 12:"Octobre 2016", 13:"Novembre 2016", 14:"Décembre 2016", \
                15:"Janvier 2017", 16:"Février 2017"}
'''
dicoTableMois = {0:"Mars 2017", 1:"Février 2017", 2:"Janvier 2017"}
dico_couleurs_candidats = {u"Arnaud Montebourg":"#CC0066", u"Benoît Hamon":"#CC3399",u"Cécile Duflot":"#008000", u"Emmanuel Macron":"#A9A9A9",
          u"François Bayrou":"#FF6600", u"François Fillon":"#3399FF", u"François Hollande":"#FF9999",  u"Jacques Cheminade":"#CC0000",
          u"Jean-Luc Mélenchon":"#FF0000", u"Manuel Valls":"#FF6699", u"Marine Le Pen":"#000080", u"Nathalie Arthaud":"#CC0033",
          u"Nicolas Dupont-Aignan":"#0000CC",  u"Nicolas Hulot":"#66CC00", u"Philippe Poutou":"#990033",
          u"Sylvia Pinel":"#FF0066", u"Yannick Jadot":"#339900"}

dico_candidat_parti = {u"Arnaud Montebourg":"PS",u"Benoît Hamon":"PS",u"Cécile Duflot":"eelv",
        u"Emmanuel Macron" : "En Marche",
          u"François Bayrou" : "MoDem",  u"François Fillon":"Les Républicains",
          u"François Hollande" : "PS", u"Jacques Cheminade" : "sp",
          u"Jean-Luc Mélenchon" : "Parti de Gauche",  u"Manuel Valls":"PS",u"Marine Le Pen":"FN",
          u"Nathalie Arthaud":"lutte ouvriere",
          u"Nicolas Dupont-Aignan":"Debout La France", u"Nicolas Hulot":"empty", u"Philippe Poutou":"NPA",
          u"Sylvia Pinel":"ps",  u"Yannick Jadot":"eelv"}


def loadHTML(URL):
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')


def loadPandas(URL):
    tables = loadHTML(URL).findAll("table")

    dfF = pd.DataFrame()
    dfFs = pd.DataFrame()

    #Pour chaque table de wikipedia :
    for idx, table in enumerate(tables) :
        lignes = table.findAll("tr")

        #On récupère le nom de chaque colonne :
        colonnes = []
        for elem in lignes[0].findAll("th"):
            if elem.find("a") is None :
                if elem.text != u'Autres candidats':
                    colonnes.append(elem.text)
            else :
                if(elem.find("a").text != ""):
                    colonnes.append(elem.find("a").text)
        for elem in lignes[1].findAll("th"):
            if elem.find("a") is not None :
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
                try:
                    while line[i] != "/":
                        i+=1
                except:
                    continue

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

        try :
            df = df[df["Date"] != "/"]
        except:
            continue

        if idx >= 0 and idx <= 2:
            df["Date"] = df["Date"].map(lambda x : x.lower().replace(dicoTableMois[idx].lower()[:-5],""))
            df["Date"] = df["Date"].map(lambda x : x+" "+dicoTableMois[idx])

        #2ème tour :
        if len(colonnes) < 7  :
            dfFs = dfFs.append(df)
        #1er tour :
        elif idx >= 0 and idx <= 2:
            dfF = dfF.append(df.ix[1:])

    return (dfF, dfFs)

dfF, dfFs = loadPandas(URL)


#######################################################################
########################### 1er tour ##################################
#######################################################################

dfF = dfF.replace(to_replace=["-", "–"], value=" ")
dfF = dfF[dfF["Pourrait changer d'avis"]!="/"]
dfF["Pourrait changer d'avis"] = dfF["Pourrait changer d'avis"].map(lambda x : (str(x).split("[")[0].strip()))

dfF["Pourrait changer d'avis"] = dfF["Pourrait changer d'avis"].map(lambda x : 0 if x == "nan" or x == "" else float(x[:2]))


notCandidats = [u"Date", u"Sondeur", u"Échantillon"]

anciensCandidats = [u"Alain Juppé", u"Bruno Le Maire", u"Jean-François Copé", u"Nicolas Sarkozy", u"Eva Joly", u"Sylvia Pinel", u"Vincent Peillon", u"Arnaud Montebourg"]

for col in dfF.columns:
    if col not in notCandidats:
        dfF[col] = dfF[col].map(lambda x: x if isinstance(x, float) else np.nan)


dfF2 = dfF
for col in anciensCandidats:
    if col in dfF2.columns :
        dfF2 = dfF2[dfF2[col].isnull()]
        dfF2 = dfF2.drop(col, axis=1)

dfF2["Pourrait changer d'avis"] = dfF2["Pourrait changer d'avis"].map(lambda x : np.nan if x==0 else x)

#print(dfF)
dfF3 = dfF2

dfF3["Date"] = dfF3["Date"].map(lambda x : x.replace("1er", "1").replace("fév.", ""))
dfF3["Date"] = dfF3["Date"].map(lambda x : ' '.join(x.split()))
dfF3["Date"] = dfF3["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[-3:]))
dfF3["Date"] = dfF3["Date"].map(lambda x : dateparser.parse(x).date())

dfF3 = dfF3.groupby(["Date"]).mean().reset_index()
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
dfF3 = dfF3[dfF3["Date"] > datetime.date(year=2017,month=01,day=01)]
dfF4 = dfF3

#dfF4 = dfF4.drop([u"Cécile Duflot", u"François Hollande", u"Nicolas Hulot", u"Rama Yade"], axis=1)

for col in dfF4.columns:
    if col not in [u"Benoît Hamon", u"Emmanuel Macron", u"Date", u"François Fillon",\
                   u"Jean-Luc Mélenchon", u"Marine Le Pen", u"Nicolas Dupont-Aignan"]:
        dfF4 = dfF4.drop(col, axis=1)

dfF5 = dfF4

dfF4["date"] = dfF4["Date"].map(lambda x: dateToString(x))
dfF4 = dfF4.drop("Date", axis=1)

dfF4 = dfF4.set_index("date")
dfF4 = dfF4.dropna(axis=1, how='all')
dfF4 = dfF4.dropna(axis=0, how='all')


# --- To json --- #

dfF5 = dfF5.dropna(axis=1, how='all')
dfF5 = dfF5.dropna(axis=0, how='all')
dfF5 = dfF5.set_index("Date")

#dfF5.to_csv("table_agrege.csv")

dfF5 = pd.read_csv("table_agrege.csv", encoding="utf-8")
dfF5["Date"] = pd.to_datetime(dfF5["Date"])
dfF5 = dfF5.groupby(["Date", "date"]).mean().reset_index()
dfF5.set_index("Date", inplace=True)

print(dfF5)

idx = pd.date_range(min(dfF5.index), max(dfF5.index))

dfF5 = dfF5.reindex(idx, fill_value="null")


########################
# Agrégats sur 6 jours #
########################
dfF5 = dfF5.drop("date", axis=1)
dfF5 = dfF5.replace(to_replace=["null"], value=np.nan)
diffDaysLast = (datetime.datetime.now()-max(dfF5.index).to_datetime()).days
#dfF5.index = dfF5.index.map(lambda x : x.to_datetime() + datetime.timedelta(days=diffDaysLast))

#dfF5 = dfF5.map(lambda x : )


lastsondages = max(dfF5.index)
to_add = (max(dfF5.index) - (max(dfF5.groupby(pd.TimeGrouper('6D')).mean().index))).days
dfF5.index = dfF5.index.map(lambda x : (x + datetime.timedelta(days=to_add)) )

dfF5 = dfF5.groupby(pd.TimeGrouper('6D')).mean()
#dfF5 = dfF5.index.map(lambda x : x.to_datetime() + datetime.timedelta(days=6))
for col in dfF5.columns :
    dfF5[col] = np.round(dfF5[col], 1)
print(dfF5)


to_json = []
dico_sondage = {}
dico_sondage["id"] = 1
dico_sondage["refresh"] = {}

dfF5 = dfF5.fillna("null")

dico_sondage["refresh"]["last"] = time.mktime((lastsondages.to_datetime()).timetuple())

dico_sondage["refresh"]["dayInterval"] = 6

dico_sondage["title"] = "Agrégation des sondages pour le 1er tour de 11 instituts*"

dico_sondage["legende"] = "* Les données de ce graphique sont les moyennes des sondages d'intentions de vote de 11 instituts sur six jours. \
Plus précisément, pour chaque jour affiché, il fait la moyenne sur les six derniers jours. \
Les instituts sont : Ifop-Fiducial, OpinionWay, CSA, Future Thinking - SSI, BVA, Odoxa, Harris Interactive, TNS Sofres, Cevipof Ipsos-Sopra Steria, Elabe, Dedicated Research."
dico_sondage["unit"] = "%"

dico_sondage["dataset"] = []



for col in dfF5.columns:
    #On garde les candidats demandés :
    dico_temp = {}
    dico_temp["title"] = col
    if col in dico_candidat_parti.keys():
        dico_temp["subtitle"] = dico_candidat_parti[col]
    else :
        dico_temp["subtitle"] = ""

    if col in dico_couleurs_candidats.keys():
        dico_temp["color"] = dico_couleurs_candidats[col]
    else :
        dico_temp["color"] = "#ffffff"

    dico_temp["data"] = list(dfF5[col])
    dico_sondage["dataset"].append(dico_temp)
to_json.append(dico_sondage)


#dfF4.to_csv(path+"sondages1er.csv", sep="\t", encoding='utf-8')

#dfF4.to_json(path1+"pollster1.json", force_ascii=False)

dfF4.to_csv(path1+"sondages1er.csv", sep="\t", encoding='utf-8')

dfF4.to_csv(path1+"data.tsv", sep="\t", encoding='utf-8')
dfF4.to_csv("data.tsv", sep="\t", encoding='utf-8')

#print(dfF3[["Manuel Valls", "Date"]])




#######################################################################
########################### 2nd tour ##################################
#######################################################################

dfFs2 = dfFs

dfFs2["Date"] = dfFs2["Date"].map(lambda x : x if len(x)>5 else np.nan)
dfFs2 = dfFs2[dfFs2["Date"].notnull()]
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x.replace(u"-", " ").replace(u"–", " "))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[-3:]))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : dateparser.parse(x).date())


#dfFs2 = dfFs2.set_index(["Date"])
#dfFs2.index = pd.to_datetime(dfFs2.index)


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
    return df[[nom1, nom2, "date"]].set_index("date").dropna(axis=0, how='any')

for col in dfFs2.columns:
    if col not in notCandidats:
        if col != "Abstention, blanc ou nul":
            dfFs2[col] = dfFs2[col].map(lambda x: x if isinstance(x, float) else np.nan)
        else :
            dfFs2[col] = dfFs2[col].map(lambda x: x if isinstance(x, float) else 0)

#dfFs2["Date"] = pd.to_datetime(dfFs2["Date"])
#dfFs2 = dfFs2.groupby(dfFs2["Date"].dt.month).mean()
#dfFs2 = dfFs2.reset_index()



dfFs2["date"] = dfFs2["Date"].map(lambda x: dateToString2(x))
dfFs2 = dfFs2.drop("Date", axis=1)

getDuel(dfFs2, u"Marine Le Pen", u"François Fillon").to_csv(path2+"mlpVSff.tsv", sep="\t", encoding="utf-8")
getDuel(dfFs2, u"Marine Le Pen", u"Manuel Valls").to_csv(path2+"mlpVSmv.tsv", sep="\t", encoding='utf-8')
getDuel(dfFs2, u"Marine Le Pen", u"Emmanuel Macron").to_csv(path2+"mlpVSem.tsv", sep="\t", encoding='utf-8')
getDuel(dfFs2, u"Emmanuel Macron", u"François Fillon").to_csv(path2+"emvsff.tsv", sep="\t", encoding="utf-8")

'''
getDuel(dfFs2, u"Marine Le Pen", u"Manuel Valls").to_json(path2+"mlpVSmv.json", force_ascii=False)
getDuel(dfFs2, u"Marine Le Pen", u"François Fillon").to_json(path2+"mlpVSff.json", force_ascii=False)
getDuel(dfFs2, u"Marine Le Pen", u"Emmanuel Macron").to_json(path2+"mlpVSem.json", force_ascii=False)
getDuel(dfFs2, u"Emmanuel Macron", u"François Fillon").to_json(path2+"emvsff.json", force_ascii=False)
'''
dfFs2.to_csv(path2+"sondages2e.csv", encoding='utf-8')
#dfFs2.to_json(path2+"sondages2e.json")
print("Done")
