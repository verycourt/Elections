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
candidates = ['Valls','Macron','Le Pen','Melenchon','Bayrou','Hamon','Fillon']
# les mots-clés dans les listes doivent rester en lower case
pseudo = {'Valls':['valls','@manuelvalls','#valls'],'Macron':['macron','#macron','@emmanuelmacron'],'Jadot':['jadot','#jadot','@yjadot'],
'Le Pen':['@mlp_officiel','#mlp','lepen'],'Melenchon':['melenchon','#melenchon','@jlmelechon'],'Bayrou':['bayrou','#bayrou','@bayrou'],
'Poutou':['poutou','#poutou','@philippepoutou'],'Peillon':['peillon','#peillon','@vincent_peillon'],'Rugy':['#rugy','rugy','@fderugy'],
'Hamon':['hamon','#hamon','@benoithamon'],'Pinel':['pinel','#pinel','@sylviapinel'],'Bennhamias':['bennhamias','#bennhamias','@jlbennhamias'],
'Montebourg':['montebourg','#montebourg','@montebourg'],'Fillon':['fillon','#fillon','@francoisfillon']}

data = {}
duplicates = []
removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]

try:
	for doc in collection.aggregate(removepipe) :
		it = iter(doc['dups'])
		next(it)
		for id in it :
			duplicates.append(pymongo.DeleteOne({'_id':id}))
	collection.bulk_write(duplicates)
except:
	pass

for i in range(18):
	for candidate in candidates:
		print(candidate)
		regexp = ''
		for p in pseudo[candidate]:
			regexp = regexp + p.lower() + "|"
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

