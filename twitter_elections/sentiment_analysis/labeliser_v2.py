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
    
    print('{} doublons retirés.'.format(count))
    client.close()

print("NB: si un tweet concerne plusieurs candidats à la fois, avec des sentiments mitigés (par exemple positif envers un candidat et negatif envers un autre), il est préférable de ne pas le labéliser (touche r).")

client = pym.MongoClient('localhost',27017)
collection = client.tweet.tweet

print('Recuperation de tweets pris au hasard dans la base...')

#corpus = collection.aggregate([{'$match':{'t_text':{'$not':re.compile('rt @')}}},{'$sample':{'size':200}},{'$project':{'t_text':1, 't_id':1}}])
corpus = collection.aggregate([{'$sample':{'size':200}},{'$project':{'t_text':1, 't_id':1}}])
client.close()

sentimentmap = {'a':1,'z':0,'e':-1}
phrase = 'Sentiment ? Positif: a , Négatif: e, Neutre: z, Ne Sais Pas / Plusieurs candidats: r, Quitter: X\n'

compte = 0
collection = client.tweet.train
for tweet in corpus:
    if 'rt @' not in tweet['t_text']:
        print(20*'-')
        print(tweet['t_text'])
        print(20*'-')
        sentiment = raw_input(phrase)
        
        while(sentiment not in ['a', 'z', 'e', 'r', 'X']) :
            print("Touche invalide. Essaie encore.\n")
            print(20*'-')
            print(tweet['t_text'])
            print(20*'-')
            sentiment = raw_input(phrase)

        if sentiment == 'r':
            continue
        elif sentiment == 'X':
            break
        else:
            collection.insert_one({'t_id':tweet['t_id'], 'text':tweet['t_text'], 'sentiment':sentimentmap[sentiment]})
            compte += 1
    else:
        continue

n_tweets = collection.count()
client.close()

print('Insertion de {0} tweets dans la base "train", qui compte desormais {1} tweets.'.format(compte, n_tweets))
retrait_doublons(collection)
print('\nMerci de ta collaboration !')