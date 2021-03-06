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

dicoTableMois = {4:"Janvier 2016", 5:"F�vrier 2016", 6:"Mars 2016", 7:"Avril 2016", 8:"Mai 2016", 9:"Juin 2016",\
                 10:"Juillet 2016", 11:"Septembre 2016", 12:"Octobre 2016", 13:"Novembre 2016", 14:"D�cembre 2016", \
                15:"Janvier 2017", 16:"F�vrier 2017"}

dico_couleurs_candidats = {u"Arnaud Montebourg":"#CC0066", u"Beno�t Hamon":"#CC3399",u"C�cile Duflot":"#008000", u"Emmanuel Macron":"#A9A9A9",
          u"Fran�ois Bayrou":"#FF6600", u"Fran�ois Fillon":"#000080", u"Fran�ois Hollande":"#FF9999",  u"Jacques Cheminade":"#CC0000",
          u"Jean-Luc M�lenchon":"#FF0000", u"Manuel Valls":"#FF6699", u"Marine Le Pen":"#3399FF",  u"Nathalie Arthaud":"#CC0033",
          u"Nicolas Dupont-Aignan":"#0000CC",  u"Nicolas Hulot":"#66CC00", u"Philippe Poutou":"#990033",
          u"Sylvia Pinel":"#FF0066", u"Yannick Jadot":"#339900"}

dico_candidat_parti = {u"Arnaud Montebourg":"ps",u"Beno�t Hamon":"ps",u"C�cile Duflot":"eelv",
        u"Emmanuel Macron" : "en marche",
          u"Fran�ois Bayrou" : "modem",  u"Fran�ois Fillon":"les republicains",
          u"Fran�ois Hollande" : "ps", u"Jacques Cheminade" : "sp",
          u"Jean-Luc M�lenchon" : "partie_de_gauche",  u"Manuel Valls":"ps",u"Marine Le Pen":"fn",
          u"Nathalie Arthaud":"lutte ouvriere",
          u"Nicolas Dupont-Aignan":"debout_la_france", u"Nicolas Hulot":"empty", u"Philippe Poutou":"npa",
          u"Sylvia Pinel":"ps",  u"Yannick Jadot":"eelv"}

def loadHTML(URL):
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')


def loadPandas(URL):
    tables = loadHTML(URL).findAll("table")

    dfF = pd.DataFrame()
    dfFs = pd.DataFrame()

    #Pour chaque table de wikipedia :
    for idx, table in enumerate(tables[29:]) :
        lignes = table.findAll("tr")

        #On r�cup�re le nom de chaque colonne :
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

        #On cr�e un pandas dataframe pour stocker nos table :
        df = pd.DataFrame(columns = colonnes)

        #print(len(colonnes))

        nbRowspan = 0
        rowspan = []
        rowspanMil = []

        #our chaque ligne de notre table :
        for j,ligne in enumerate(lignes[2:]):
            line = list(np.zeros(len(colonnes)))
            line = ["/" for item in line]

            #lorsque certains �l�ments de notre tableau occupent plusieurs lignes
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

        df = df[df["Date"] != "/"]
        if idx+14 >= 4 and idx+14 <= 16:
            df["Date"] = df["Date"].map(lambda x : str(x)+" "+dicoTableMois[idx+14])

        #2�me tour :
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

dfF = dfF.replace(to_replace=["-", "�"], value=" ")
print(dfF.columns)
dfF["Pourrait changer d'avis"] = dfF["Pourrait changer d'avis"].map(lambda x : (str(x).split("[")[0].strip()))

notCandidats = [u"Date", u"Sondeur", u"�chantillon"]

anciensCandidats = [u"Alain Jupp�", u"Bruno Le Maire", u"Jean-Fran�ois Cop�", u"Nicolas Sarkozy", u"Eva Joly", u"Sylvia Pinel", u"Vincent Peillon", u"Arnaud Montebourg"]

for col in dfF.columns:
    if col not in notCandidats:
        dfF[col] = dfF[col].map(lambda x: x if isinstance(x, float) else np.nan)


dfF2 = dfF
for col in anciensCandidats:
    if col in dfF2.columns:
        dfF2 = dfF2[dfF2[col].isnull()]
        dfF2 = dfF2.drop(col, axis=1)

dfF2["Pourrait changer d'avis"] = dfF2["Pourrait changer d'avis"].map(lambda x : np.nan if x==0 else x)

#print(dfF)
dfF3 = dfF2

dfF3["Date"] = dfF3["Date"].map(lambda x : x.replace("1er ", "1").replace("f�v.", ""))
dfF3["Date"] = dfF3["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[-3:]))
dfF3 = dfF3.drop(dfF3.index[3])
print(dfF3["Date"])

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

dfF4 = dfF4.drop([u"C�cile Duflot", u"Fran�ois Hollande", u"Nicolas Hulot", u"Rama Yade"], axis=1)

for col in dfF4.columns:
    if col not in [u"Beno�t Hamon", u"Emmanuel Macron", u"Date", u"Fran�ois Fillon",\
                   u"Jean-Luc M�lenchon", u"Marine Le Pen", u"Philippe Poutou"]:
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
idx = pd.date_range(min(dfF5.index), max(dfF5.index))

dfF5 = dfF5.reindex(idx, fill_value="null")

########################
# Agr�gats sur 6 jours #
########################
dfF5 = dfF5.drop("date", axis=1)
dfF5 = dfF5.replace(to_replace=["null"], value=np.nan)

dfF5 = dfF5.groupby(pd.TimeGrouper('6D')).mean()

for col in dfF5.columns :
    dfF5[col] = np.round(dfF5[col], 1)
print(dfF5)



to_json = []
dico_sondage = {}
dico_sondage["id"] = 1
dico_sondage["refresh"] = {}
print(dfF5.columns)

dfF5 = dfF5.fillna("null")

dico_sondage["refresh"]["last"] = time.mktime((max(dfF5.index).to_datetime()).timetuple())

dico_sondage["refresh"]["dayInterval"] = 6

dico_sondage["title"] = "Agr�gation des sondages sur le 1er tour de 11 instituts*"

dico_sondage["legende"] = "* Les donn�es de ce graphique sont les moyennes des sondages de 11 instituts \
sur six jours. Plus pr�cis�ment, il fait donc, pour chaque jour affich�, la moyenne sur les six derniers jours.\
Les instituts sont : Ifop-Fiducial, OpinionWay, CSA, Future Thinking - SSI, BVA, Odoxa, Harris Interactive, TNS Sofres, Cevipof Ipsos-Sopra Steria, Elabe, Dedicated Research."
dico_sondage["unit"] = "%"

dico_sondage["dataset"] = []


for col in dfF5.columns:
    #On garde les candidats demand�s :
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

with open(path1+'data.json', 'w') as fp:
    json.dump(dico_sondage, fp, ensure_ascii=False)

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
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x.replace(u"-", " ").replace(u"�", " "))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : x if len(x.split(" ")) < 4 else " ".join(x.split(" ")[-3:]))
dfFs2["Date"] = dfFs2["Date"].map(lambda x : dateparser.parse(x).date())


#dfFs2 = dfFs2.set_index(["Date"])
#dfFs2.index = pd.to_datetime(dfFs2.index)


notCandidats = [u"Date", u"Sondeur", u"�chantillon"]

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

getDuel(dfFs2, u"Marine Le Pen", u"Fran�ois Fillon").to_csv(path2+"mlpVSff.tsv", sep="\t", encoding="utf-8")
getDuel(dfFs2, u"Marine Le Pen", u"Manuel Valls").to_csv(path2+"mlpVSmv.tsv", sep="\t", encoding='utf-8')
getDuel(dfFs2, u"Marine Le Pen", u"Emmanuel Macron").to_csv(path2+"mlpVSem.tsv", sep="\t", encoding='utf-8')
getDuel(dfFs2, u"Emmanuel Macron", u"Fran�ois Fillon").to_csv(path2+"emvsff.tsv", sep="\t", encoding="utf-8")

'''
getDuel(dfFs2, u"Marine Le Pen", u"Manuel Valls").to_json(path2+"mlpVSmv.json", force_ascii=False)
getDuel(dfFs2, u"Marine Le Pen", u"Fran�ois Fillon").to_json(path2+"mlpVSff.json", force_ascii=False)
getDuel(dfFs2, u"Marine Le Pen", u"Emmanuel Macron").to_json(path2+"mlpVSem.json", force_ascii=False)
getDuel(dfFs2, u"Emmanuel Macron", u"Fran�ois Fillon").to_json(path2+"emvsff.json", force_ascii=False)
'''
dfFs2.to_csv(path2+"sondages2e.csv", encoding='utf-8')
#dfFs2.to_json(path2+"sondages2e.json")
print("Done")
