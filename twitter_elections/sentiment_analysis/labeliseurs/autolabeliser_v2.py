#!/usr/bin/python
#-*- coding: utf-8 -*-

import pymongo as pym
import re

def insert_tweets_in_mongo(candidates, sentiment, limit=1000):
    '''Echelle de classification -1 Négatif 0 Neutre 1 Positif
    Critère de sélection d'un tweet : ne doit pas être un retweet, ne doit contenir le nom 
    que d'un seul candidat'''
    
    # le (?i) rend la regex insensible a la casse. Il ne faut pas laisser de liste vide
    # sinon l'algo va tirer n'importe quel tweet dans la base sans filtre particulier
    if sentiment=='neg':
        val = -1
        dico = {'fillon': '(?i)#penelopegate|#fillongate|#fillondemission',
             'macron': '(?i)#stopmacron||#lepionmacron|#macrongate|#hollandebis|#macrongirouette|#toutsaufmacron',
             'le pen': '(?i)#lepengate|#fngate',
             'hamon': '(?i)#bilalhamon|#plusjamaisps|#hamonpiègeacons',
             'melenchon': '(?i)#placeholder_pour_melenchon_negatif'}
    elif sentiment=='pos':
        val = 1
        dico = {'fillon': '(?i)#stopchassealhomme|#fillonpresident|#projetfillon|#soutienfillon',
             'macron': '(?i)#teammacron|#lafranceenmarche',
             'hamon': '(?i)#hamonpresident|#avechamon|#jevotepour',
             'le pen' : '(?i)#aunomdupeuple|#jechoisismarine',
             'melenchon': '(?i)#6erépublique|#6erepublique|#placeaupeuple|#CantStenchonTheMelenchon|#18mars2017'}
    elif sentiment=='neu':
        # TODO: pour les neutres, envisager de récupérer les tweets de médias via les @
        val = 0
        dico = {'fillon': '(?i)#confpressfillon|#conffillon',
            'macron': '(?i)#macronlyon',
            'le pen': '(?i)#placeholder_pour_lepen_neutre',
            'hamon': '(?i)#placeholder_pour_hamon_neutre',
            'melenchon': '(?i)#placeholder_pour_melenchon_neutre'}
    else:
        print('Choisir le sentiment parmi "neg", "pos" et "neu".')
        return
    
    client = pym.MongoClient()
    client = pym.MongoClient('localhost', 27017)
    collection = client.tweet.tweet
    labelisedCollection = client.tweet.labelised
    
    count = 0
    
    for candidate in candidates:
        a_inserer = []
        sentiment_regex = re.compile((dico[candidate]))
        stop_words = '|'.join([cand for cand in candidates if cand!=candidate])
        print('Regex :', dico[candidate])
        print('Stop words :', stop_words)
        
        # filtrage des retweets en amont
        corpus = collection.find(
            filter={'$and': [{'t_text': {'$not': re.compile("^rt @")}},
                             {'t_text': sentiment_regex}, {'t_text': {'$not': re.compile(stop_words)}}]},
            projection={'_id':False, 't_id':1, 't_text':1}, limit=limit)

        for t in corpus: 
            a_inserer.append({'text': t['t_text'], 'sentiment': val, 'candidat': candidate,
                             't_id': t['t_id']})
        
        labelisedCollection.insert_many(a_inserer)
        print(len(a_inserer), 'insertions effectuees.')
        count += len(a_inserer)
        
    print(45 * '-')
    print(count, 'insertions au total.')

    # retrait des doublons
    print('Retrait des doublons...')
    duplicates = []
    removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},
                             "count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]
    count = 0
    try :
        for doc in labelisedCollection.aggregate(removepipe):
            it = iter(doc['dups'])
            next(it)
            for id in it :
                count += 1
                duplicates.append(pym.DeleteOne({'_id':id}))
            if duplicates:    
                labelisedCollection.bulk_write(duplicates)    
    except:
        pass
    
    print(count, 'doublons retirés.')
    print(labelisedCollection.count(), 'tweets dans la base auto.')
    client.close()
    
    return

candidates = ['fillon', 'macron', 'le pen', 'hamon', 'melenchon']
insert_tweets_in_mongo(candidates, sentiment='pos', limit=200)