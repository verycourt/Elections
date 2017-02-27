# coding: utf-8
import pymongo as pym

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

print("Removing duplicates....\n")
removeDuplicates()
print("Done\n")

f = open('indexlabelised','r')
session = int(input("Combien de tweets à labeliser pour cette session ?\n"))
if session == 0 : exit()
index = int(f.read())
f.close()
print("Index : " + str(index) +'\n')
client = pym.MongoClient('localhost',27017)
collection = client.tweet.tweet
corpus = collection.find({'t_text':{'$regex':'^(?!.*rt).*$'}},{'t_text':1}).sort('_id',1)[index+1:index+session]
client.close()
sentimentmap = {'a':1,'z':0,'e':-1}
for i, tweet in enumerate(corpus):
    currtweet = {}
    print(tweet['t_text'])
    sentiment = raw_input('Sentiment ? Positif : a , Négatif : e, Neutre : z ')
    while(sentiment not in ['a','z','e']) :
        print("erreur\n")
        sentiment = raw_input('Sentiment ? Positif : a , Négatif : e, Neutre : z ')
    labeled = {'text':tweet['t_text'],'sentiment':sentimentmap[sentiment]}
    f = open('indexlabelised','w')
    f.write(str(int(index)+i))
    f.close()
    client = pym.MongoClient('localhost',27017)
    collection = client.tweet.train
    collection.insert_one(labeled)
    client.close()
