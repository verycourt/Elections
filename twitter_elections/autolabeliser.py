#!/usr/bin/python
#-*- coding: utf-8 -*-

import pymongo as pym
import re

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

def getTweets(candidates, aliases, sentimentlist, sentiment):
    '''Echelle de classification -1 Négatif 0 Neutre 1 Positif critère de sélection d'un tweet : ne doit pas être un retweet, ne doit contenir le nom 
    que d'un seul candidat'''
    client = pym.MongoClient()
    source = client.tweet.tweet
    numbcand = len(candidates)
    for _ in range(numbcand) :
        currcand = candidates.pop(0)
        candRegex = ''.join(a for a in aliases[currcand])
        print('Looking for '+ candRegex + '\n')
        candRegex = re.compile(candRegex)
        sentRegex = ''.join(s for s in sentimentlist[currcand])
        print('sentiment : ', sentRegex)
        sentRegex = re.compile(sentRegex)
        notSeekedRegex = ' | '.join([aliases[cand] for cand in candidates])
        print('Without '+ notSeekedRegex + '\n')
        notSeekedRegex = re.compile(notSeekedRegex)
        aggregation = [{'$match':{'$and':[{'t_text':candRegex},{'t_text' :{'$not':notSeekedRegex}},
		{'t_text':sentRegex}]}},{'$sort':{'t_time':-1}},{'$limit':1000},{'$project':{'t_text':1, 't_id':1,'_id':False}}]
        corpus = list(source.aggregate(aggregation))
        client.close()

        for t in corpus : 
            t['sentiment'] = sentiment
            t['candidat'] = currcand

        client = pym.MongoClient()
        labelisedCollection = client.tweet.labelised
        labelisedCollection.update_many(corpus)
        client.close()
        candidates.append(currcand)

        
candidates = ['fillon','macron','le pen','hamon','melenchon']

aliases = {'fillon':'fillon | ff | lr | republicains | républicains', 'macron':'macron | enmarche',
'le pen':'mlp | marine | lepen | fn | front national | le pen','hamon':'benoit | hamon | ps | socialiste',
'melenchon':'mélenchon | jlm | jean-luc | melenchon'}  

negatives = {'fillon':'#penelopegate | #fillongate | #penelope','macron':'#stopmacron | #levraimacron | #lepionmacron | #macrongate',
'le pen':'#lepengate | #fngate | nazi | facho','hamon':'#bilalhamon | #plusjamaisps','melenchon':' goulag | bolchevisme | ruine | dictateur'}

neutrals = {'fillon':'#confpressfillon | #conffillon | #franceinfo','macron':'#ifop | #match | #macronlyon','le pen':'#rolling | #ifop',
'hamon':'#primairesgauche | #grandjury','melenchon':'#ifop | sondage'}

positives = {'fillon':'#fillon2017 | #stopchassealhomme | #fillonpresident | #projetfillon', 'macron':'#enmarche | #teammacron',
'hamon':'#avenirencommun | #rassemblement', 'le pen' : 'patriote | #aunomdupeuple | #marine2017',
 'melenchon':'#presidentielle2017 | #franceinsoumise | #jlm2017 | #placeaupeuple'}

getTweets(candidates, aliases, negatives, -1)
getTweets(candidates, aliases, neutrals, 0)
getTweets(candidates, aliases, positives, 1)


