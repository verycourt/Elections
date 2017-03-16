# coding: utf-8
import pymongo as pym
import re


def retrait_doublons(collection):
    print('Retrait d\'eventuels doublons...')
    textCleanPipeline = [{"$group":{"_id":"$text", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]
    duplicates = []
    count = 0
    try:
        for doc in collection.aggregate(textCleanPipeline) :
            it = iter(doc['dups'])
            next(it)
            for id in it:
                count += 1
                duplicates.append(pym.DeleteOne({'_id':id}))
        if duplicates:
            collection.bulk_write(duplicates)
    except:
        pass
    
    print(count, 'doublons retirés.')
    client.close()

print("NB: si un tweet concerne plusieurs candidats à la fois, il est préférable de ne pas le labéliser (touche r).")

compte = 0
labeled = []

client = pym.MongoClient('localhost',27017)
collection = client.tweet.tweet

print('Recuperation de tweets pris au hasard dans la base...')

#corpus = collection.aggregate([{'$match':{'t_text':{'$not':re.compile('rt @')}}},{'$sample':{'size':200}},{'$project':{'t_text':1, 't_id':1}}])
corpus = collection.aggregate([{'$sample':{'size':200}},{'$project':{'t_text':1, 't_id':1}}])
client.close()

sentimentmap = {'a':1,'z':0,'e':-1}
phrase = 'Sentiment ? Positif: a , Négatif: e, Neutre: z, Ne Sais Pas / Plusieurs candidats: r, Quitter: X'

for tweet in corpus:
    if 'rt @' not in tweet['t_text']:
        print(tweet['t_text'])
        sentiment = raw_input(phrase)
        
        while(sentiment not in ['a', 'z', 'e', 'r', 'X']) :
            print("Touche invalide. Essaie encore.\n")
            sentiment = raw_input(phrase)

        if sentiment == 'r':
            continue
        elif sentiment == 'X':
            break
        else:
            labeled.append({'t_id':tweet['t_id'], 'text':tweet['t_text'], 'sentiment':sentimentmap[sentiment]})
            compte += 1
    else:
        continue

collection = client.tweet.train
collection.insert_many(labeled)
n_tweets = collection.count()
client.close()

print('Insertion de {0} tweets dans la base "train", qui compte desormais {1} tweets'.format(compte, n_tweets))
retrait_doublons(collection)