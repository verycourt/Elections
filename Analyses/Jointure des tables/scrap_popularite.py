import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from dateutil import relativedelta

import dateparser
import datetime
import warnings
warnings.filterwarnings('ignore')

URL = "http://www.tns-sofres.com/cotes-de-popularites"

resultats = requests.get(URL)
page = BeautifulSoup(resultats.text, 'html.parser')

presidents = page.find_all("tr")
#print(presidents[3].findAll("td"))
code_prez = []

for i in range(1,12,2):
    code_prez.append(presidents[i].findAll("td")[1].find_all("a", href=True)[0]["href"].split("code_nom=")[1])

print(code_prez)

url_code = "http://www.tns-sofres.com/dataviz?type=1&code_nom="

dfF = pd.DataFrame(columns=["President", "Confiance", "Pas Confiance"])

for code in code_prez:
    df = pd.DataFrame(columns=["Date", "Confiance", "Pas Confiance"])
    print(df.shape)
    resultats = requests.get(url_code+code)
    page = BeautifulSoup(resultats.text, 'html.parser')

    for table in page.find_all("table"):
        for tr in table.find_all("tr")[2:]:
            data = []
            for td in tr.find_all("td")[:5:2]:
                data.append(td.text)
            df.loc[df.shape[0]] = data

    df = df[(df["Date"] != "---") & (df["Confiance"] != "-")]
    df["Date"] = df["Date"].map(lambda x: dateparser.parse(x))
    max_date = max(df["Date"])
    df = df[df["Date"] == max_date - relativedelta.relativedelta(months=5)]
    df = df.drop_duplicates()
    df["Date"] = code
    df = df.rename(columns={'Date': 'President'})

    dfF = pd.concat([dfF, df])
print(dfF)
dfF.to_csv("popularite.csv")
