# coding: utf-8
import pymongo as pym
import re

''' Récupérer X tweets à labelliser
afficher les tweets un par un,  
prendre en input le sentiment
insérer le tweet labelisé dans une autre collection'''

def removeDuplicates():
	client = pym.MongoClient()
        c = client.tweet.tweet
	duplicates = []
	removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]
	try :
		for doc in c.aggregate(removepipe) :
			it = iter(doc['dups'])
			next(it)
			for id in it :
				duplicates.append(pym.DeleteOne({'_id':id}))
		c.bulk_write(duplicates)	
	except:
		pass
        client.close()

#print("Removing duplicates....\n")
#removeDuplicates()
#print("Done\n")
print("NB: si un tweet concerne plusieurs candidats à la fois, il est préférable de ne pas le labéliser.")

session = int(input("Combien de tweets à labeliser pour cette session ?\n"))
if session == 0 : exit()
client = pym.MongoClient('localhost',27017)
collection = client.tweet.tweet
#corpus = collection.find({'t_text':{'$regex':'^(?!.*rt).*$'},'t_id':{'$gte':rd.random()*collection.count()-session}},{'t_text':1})[:session]
corpus = collection.aggregate([{'$match':{'t_text':{'$not':re.compile('rt @')}}},{'$sample':{'size':session}},{'$project':{'t_text':1}}])
client.close()
sentimentmap = {'a':1,'z':0,'e':-1}
phrase = 'Sentiment ? Positif : a , Négatif : e, Neutre : z, Ne Sais Pas / Plusieurs candidats : r '

collection = client.tweet.train
for i, tweet in enumerate(corpus):
    currtweet = {}
    print(tweet['t_text'])
    sentiment = raw_input(phrase)
    
    while(sentiment not in ['a','z','e','r']) :
        print("erreur\n")
        sentiment = raw_input(phrase)

    if sentiment == 'r' : continue

    labeled = {'text':tweet['t_text'],'sentiment':sentimentmap[sentiment]}
    collection.insert_one(labeled)

client.close()
