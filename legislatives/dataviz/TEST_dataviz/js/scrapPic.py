from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Pool

page = 'http://www2.assemblee-nationale.fr/deputes/liste/alphabetique'
base = 'http://www2.assemblee-nationale.fr'
response = BeautifulSoup(requests.get(page).text, 'html.parser')
divs = response.find_all('div', class_="clearfix col-container")
lis = []
for div in divs:
	lis.extend(div.find_all('li'))
export = {}

for li in lis:
	a = li.find("a", href=True)
	req = BeautifulSoup(requests.get(base+a["href"]).text, 'html.parser')
	img = req.find_all("img")[1]['src']
	export[a.text] = base+img
	print(a.text + ' ' + base+img)

with open("gueules_deputes.json", "w") as fdp:
	json.dump(export, fdp)
print(len(export))
