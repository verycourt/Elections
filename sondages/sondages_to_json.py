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

warnings.filterwarnings('ignore')


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

with open(path1+'data.json', 'w') as fp:
    json.dump(dico_sondage, fp, ensure_ascii=False)

#dfF4.to_csv(path+"sondages1er.csv", sep="\t", encoding='utf-8')

#dfF4.to_json(path1+"pollster1.json", force_ascii=False)


#print(dfF3[["Manuel Valls", "Date"]])



print("Done")
