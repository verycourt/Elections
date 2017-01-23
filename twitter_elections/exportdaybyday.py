#!/usr/bin/python	
# -*- coding: latin-1 -*-
import pymongo
import json
import time

now = time.time() * 1000
from pprint import pprint

from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
candidates = ['Valls','Macron','Le Pen','Jadot','Melenchon','Bayrou','Poutou','Peillon','Rugy','Hamon','Pinel','Bennhamias','Montebourg','Fillon']
pseudo = {'Valls':['valls','@manuelvalls','#valls'],'Macron':['macron','#macron','@EmmanuelMacron'],'Jadot':['Jadot','#Jadot','@yjadot'],
'Le Pen':['@MLP_officiel','#MLP','lepen'],'Melenchon':['Melenchon','#Melenchon','@JLMelechon'],'Bayrou':['Bayrou','#Bayrou','@bayrou'],
'Poutou':['Poutou','#Poutou','@PhilippePoutou'],'Peillon':['Peillon','#peillon','@Vincent_Peillon'],'Rugy':['#Rugy','Rugy','@FdeRugy'],
'Hamon':['Hamon','#hamon','@benoithamon'],'Pinel':['pinel','#pinel','@SylviaPinel'],'Bennhamias':['bennhamias','#bennhamias','@JLBennhamias'],
'Montebourg':['montebourg','#montebourg','@montebourg'],'Fillon':['Fillon','#Fillon','@FrancoisFillon']}

data = {}
duplicates = []
removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]

for doc in collection.aggregate(removepipe) :
	it = iter(doc['dups'])
	next(it)
	for id in it :
		duplicates.append(pymongo.DeleteOne({'_id':id}))
collection.bulk_write(duplicates)	

for i in range(18):
	for candidate in candidates:
		print(candidate)
		regexp = ''
		for p in pseudo[candidate]:
			regexp = regexp + p + "|"
		regexp = regexp[:-1]
		print(regexp)
		pipe = [
		{
			"$match":
				{
					"$and":
					[
						{
							"t_text":
								{
									"$regex":regexp
								}
						},
						{
							"$and":
								[
								{
									"t_time":
											{
												"$gte":now - (i+1)*8.64e7
											}
								},
								{
									"t_time":
											{
												"$lte":now - i*8.64e7
											}
								}
								]
						}
					]
				}
		},
		{
			"$group":
				{
					"_id":candidate,"total":
								{
									"$sum":1
								}
				}
		}
]
		result = list(collection.aggregate(pipeline=pipe))
		try :
			data[candidate] = {"name":candidate,"size": result[0]["total"]}
			print(data[candidate])
		except : print("no tweet")
	print(data)
	export = {"name":"twitter_mentions","children":[entry for entry in data.values()]}
	print(export)
	file = open('/var/www/html/decompte/j-'+str(i+1)+'.json','w')
	json.dump(export,file) 
	file.close()

