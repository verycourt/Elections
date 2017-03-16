#!/usr/bin/python
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymongo
import json
import time

now = time.time() * 1000
from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
candidates = [u'François Fillon',u'Benoît Hamon','Marine Le Pen','Emmanuel Macron',u'Jean-Luc Mélenchon']
parties = ['LR','PS','FN','En Marche!','PG']
colors = ["#000080", "#CC3399", "#3399FF", "#A9A9A9", "#FF0000"]
pseudo = {'Valls':['valls','@manuelvalls','#valls'],'Emmanuel Macron':['macron','#macron','@EmmanuelMacron'],'Jadot':['Jadot','#Jadot','@yjadot'],
'Marine Le Pen':['le pen', 'mlp','lepen'],u'Jean-Luc Mélenchon':['Melenchon','#Melenchon','@JLMelechon'],'Bayrou':['Bayrou','#Bayrou','@bayrou'],'Arthaud':['arthaud'],
'Poutou':['Poutou','#Poutou','@PhilippePoutou'],'Peillon':['Peillon','#peillon','@Vincent_Peillon'],'Rugy':['#Rugy','Rugy','@FdeRugy'],
u'Benoît Hamon':['Hamon','#hamon','@benoithamon'],'Pinel':['pinel','#pinel','@SylviaPinel'],'Bennhamias':['bennhamias','#bennhamias','@JLBennhamias'],
'Montebourg':['montebourg','#montebourg','@montebourg'],u'François Fillon':['Fillon','#Fillon','@FrancoisFillon']}

data = {}
dataLePoint = {}
duplicates = []
removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]

try :
	for doc in collection.aggregate(removepipe) :
		it = iter(doc['dups'])
		next(it)
		for id in it :
			duplicates.append(pymongo.DeleteOne({'_id':id}))
	collection.bulk_write(duplicates)	
except:
	pass

for idx, candidate in enumerate(candidates):
	print(candidate)
	regexp = ''
	for p in pseudo[candidate]:
		regexp = regexp + p.lower() + "|"
	regexp = regexp[:-1]
	print(regexp)
	pipe = [{"$match":{"$and":[{"t_text":{"$regex":regexp}},{"t_time":{"$gte":now - 2.592e8}}]}},{"$group":{"_id":candidate,"total":{"$sum":1}}}]
	result = list(collection.aggregate(pipeline=pipe))
	try :
		data[candidate] = {"name":unicode(" ".join(candidate.split()[1:])),"size": result[0]["total"]}
		dataLePoint[candidate] = {"title":unicode(candidate),"subtitle":unicode(parties[idx]),"data": result[0]["total"],"color": colors[idx]}
		print(dataLePoint[candidate])
	except : print("no tweet")
#print(data)
print(dataLePoint)
export = {"name":"twitter_mentions","children":[entry for entry in data.values()]}
exportLePoint = {
	"title":u"Les candidats les plus mentionnés sur Twitter*",
	"legend":"* Nombre de mentions Twitter par candidat sur 3 jours glissants, rafraîchi tous les jours à 8h.",
    "id": 1,
    "unit": "nombre de tweets",
	"dataset":[entry for entry in dataLePoint.values()]
	}
print(exportLePoint)

file = open('/var/www/html/decompte/popcontest.json','w')
json.dump(export,file)
file.close()

fileLePoint = open('/var/www/html/decompte/dataTwitter3jours.json','w')
json.dump(exportLePoint,fileLePoint)
fileLePoint.close()
