# coding: utf-8
import pymongo as pym

''' Récupérer X tweets à labelliser
afficher les tweets un par un,  
prendre en input le sentiment
insérer le tweet labelisé dans une autre collection'''
f = open('indexlabelised','r')
session = int(input("Combien de tweets à labeliser pour cette session ?"))
index = int(f.read()[0])
f.close()
client = pym.MongoClient('localhost',27017)
collection = client.tweet.tweet
corpus = collection.find({'t_text':{'$regex':'^(?!.*rt).*$'}},{'t_text':1})[index:index+session]
client.close()
sentimentmap = {'a':1,'z':0,'e':-1}
for i, tweet in enumerate(corpus[:10]):
    print(tweet['t_text'])
    tweet['sentiment'] = input('Sentiment ? Positif : a , Négatif : e, Neutre : z ')
    while(tweet['sentiment'] not in ['a','z','e']) :
        print("erreur\n")
        tweet['sentiment'] = input('Sentiment ? Positif : a , Négatif : e, Neutre : z ')
    labeled = {'text':tweet['t_text'],'sentiment':sentimentmap[tweet['sentiment']]}
    f = open('indexlabelised','w')
    f.write(str(int(index)+i))
    f.close()
    client = pym.MongoClient('localhost',27017)
    collection = client.tweet.train
    collection.insert_one(labeled)
    client.close()
