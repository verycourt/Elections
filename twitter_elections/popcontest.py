#!/usr/bin/python
# -*- coding: latin-1 -*-
import pymongo
import json

from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
candidates = ['Valls','Macron','MLP','Jadot','Melenchon','Bayrou','Poutou','Peillon','Rugy','Hamon','Pinel','Bennhamias','Montebourg','Fillon']
pseudo = {'Valls':['valls','@manuelvalls','#valls'],'Macron':['macron','#macron','@EmmanuelMacron'],'Jadot':['Jadot','#Jadot','@yjadot'],
'MLP':['@MLP_officiel','#MLP','lepen'],'Melenchon':['Melenchon','#Melenchon','@JLMelechon'],'Bayrou':['Bayrou','#Bayrou','@bayrou'],
'Poutou':['Poutou','#Poutou','@PhilippePoutou'],'Peillon':['Peillon','#peillon','@Vincent_Peillon'],'Rugy':['#Rugy','Rugy','@FdeRugy'],
'Hamon':['Hamon','#hamon','@benoithamon'],'Pinel':['pinel','#pinel','@SylviaPinel'],'Bennhamias':['bennhamias','#bennhamias','@JLBennhamias'],
'Montebourg':['montebourg','#montebourg','@montebourg'],'Fillon':['Fillon','#Fillon','@FrancoisFillon']}

data = {}

for candidate in candidates:
	print(candidate)
	regexp = ''
	for p in pseudo[candidate]:
		regexp = regexp + p + "|"
	regexp = regexp[:-1]
	print(regexp)
	pipe = [{"$match":{"t_text":{"$regex":regexp}}},{"$group":{"_id":candidate,"total":{"$sum":1}}}]
	result = list(collection.aggregate(pipeline=pipe))
	data[candidate] = {"name":candidate,"size": result[0]["total"]}
	print(data[candidate])
print(data)
export = {"name":"twitter_mentions","children":[entry for entry in data.values()]}
print(export)
file = open('popcontest.json','w')
json.dump(export,file) 
file.close()
