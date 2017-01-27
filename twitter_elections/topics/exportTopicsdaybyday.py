#!/usr/bin/python	
# -*- coding: latin-1 -*-
import pymongo
import json
import time
import datetime

now = int(time.time()) * 1000
#dayNow = datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%Y')
#dayNow = time.localtime(int(time.time()))
#nowMidnightTmp = int(time.mktime(dayNow)) * 1000
#nowMidnightTmp = datetime.datetime.strptime(dayNow, "%d/%m/%Y").timestamp() * 1000

#print(dayNow)

from pprint import pprint

from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
candidates = ['Valls','Hamon','Fillon']
topics = ['travail']
# les mots-clés dans les listes doivent rester en lower case
pseudo = {'Valls':['valls','@manuelvalls','#valls'],'Hamon':['hamon','#hamon','@benoithamon'],'Fillon':['fillon','#fillon','@francoisfillon']}
topicsWords = {'travail':['#revenuuniversel','revenu', 'universel', 'salaire', 'minimum', 'pauvrete', 'seuil', 'pouvoir d\'achat', 'made in france', 'frenchtech']}

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

for i in range(6):

	startTmp = now - (i+1)*8.64e7
	endTmp = now - i*8.64e7
	
	#startTmp = nowMidnightTmp - (i+1)*8.64e7
	#endTmp = nowMidnightTmp - i*8.64e7

	# take the time of execution to get the current days' data
	#if i == 0:
		#startTmp = nowMidnightTmp
		#endTmp = now

	for candidate in candidates:
		print(candidate)

		# regex candidate
		regexp = ''
		for p in pseudo[candidate]:
			regexp = regexp + p.lower() + "|"
		# get rid of last pipe
		regexp = regexp[:-1]
		print(regexp)

		# regex on a topic
		regexTopic = ''
		for p in topicsWords['travail']:
			regexTopic = regexTopic + p.lower() + "|"
		# get rid of last pipe
		regexTopic = regexTopic[:-1]
		print(regexTopic)
		
		pipe = [
		{
			"$match":
				{
					"$and":
						[
						{
							"$and":
								[
								{
									"t_text":
										{
											"$regex":regexp
										}
								},
								{	"t_text":
										{
											"$regex":regexTopic
										}
								}
								]
						},
						{
							"$and":
								[
								{
									"t_time":
											{
												"$gte":startTmp
											}
								},
								{
									"t_time":
											{
												"$lte":endTmp
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
	file = open('/var/www/html/decompte/topics/j-'+str(i+1)+'.json','w')
	json.dump(export,file) 
	file.close()

