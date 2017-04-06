#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
import treetaggerwrapper
import pymongo as pym
import re
import string
import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import date, datetime, timedelta


def timestamp(self):
    "Return POSIX timestamp as float"
    return time.mktime((self.year, self.month, self.day,
        self.hour, self.minute, self.second,
        -1, -1, -1)) + self.microsecond / 1e6


def process_texts(list_of_texts, pos_tag_list, stop_words):
    # Processing the tweets (POS tagging, lemmatization)
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',
        TAGDIR='/home/ubuntu/Elections/twitter_elections/sentiment_analysis'
        )
    list_of_processed_texts = []
    
    for text in list_of_texts:
        # Etape de filtrage
        text = re.sub(r'\w*…', '', text) # mot tronqué par Twitter
        text = re.sub(r'(?:htt)\S*', '', text) # retrait des liens http
        text = re.sub(r'\n', ' ', text) # retrait des sauts de ligne
        text = re.sub(r'\xad', '-', text)
        text = re.sub(r'@\w*', '', text) # retrait des mentions @ (ne détecte pas @XXX@...)
        text = re.sub(r'\.{3,}', '...', text) # ....... => points de suspension
        text = re.sub(r'(?=\.\w)(\.)', '. ', text) # remplacer un point entre deux mots 'A.B' par 'A. B'
        text = re.sub(r'^rt.*: ', '', text) # retrait de la mention retweet
        #text = re.sub(r'\d', '', text) # retrait des chiffres
        
        tags = tagger.tag_text(text)
        try:
            tagged_text = ['{}|{}'.format(t.split('\t')[1], t.split('\t')[2]) for t in tags
                           if (t.split('\t')[2] not in stop_words
                               and t.split('\t')[1] in pos_tag_list)]
        except:
            tagged_text = ['ERREUR']
        list_of_processed_texts.append(tagged_text)
        
    return list_of_processed_texts


def build_Xy(df_tweets, drop_dups=False, vocab=None, min_df=5, n_grams=(1,1)):
    # Choix des tags et stop words
    pos_tags_to_keep = ['ADJ', 'ADV', 'NOM', 'NUM', 'PUN:cit', 'INT', 'DET:POS', 'PRO:POS', 'PRO:DEM',
                    'VER:cond', 'VER:futu', 'VER:impe', 'VER:impf',
                    'VER:pper', 'VER:ppre', 'VER:pres', 'VER:simp', 'VER:subi', 'VER:subp']
    stops = set(list('abcdefghijklmnopqrstuvwxyz'))

    print('Tagging des tweets en cours...')
    tweet_list = process_texts(df_tweets['text'], pos_tags_to_keep, stops)
    print('TreeTagger a renvoye {} erreur(s).'.format(tweet_list.count('ERREUR')))
    
    # Building TF-IDF matrix
    print('Creation de la matrice de features...')
    vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', decode_error='strict',
                                 lowercase=False, use_idf=False, norm=None, binary=False, vocabulary=vocab,
                                 min_df=min_df, max_df=1.0, ngram_range=n_grams)
    
    mat = vectorizer.fit_transform([' '.join(tweet) for tweet in tweet_list])
    del tweet_list
    voca = vectorizer.vocabulary_
    print('Longueur du vocabulaire : {}'.format(len(voca)))
    X = pd.DataFrame(mat.toarray())
    del mat

    # ajout colonnes features supplémentaires
    X['#'] = np.array([t.count('#') / 2. for t in df_tweets['text']])
    X['http'] = np.array([(t.count('http') / 2.) if t.count('http') > 1 else 0 for t in df_tweets['text']])
    X['@'] = np.array([t.count('@') / 1. for t in df_tweets['text']])
    X['n_car'] = np.array([np.log(len(t))/4 / 1. for t in df_tweets['text']])
    X['n_words'] = np.array([np.log(len(t.split(' '))) / 2 for t in df_tweets['text']])
    X[':'] = np.array([t.count(':') / 1. for t in df_tweets['text']])
    X['!'] = np.array([t.count('!') / 1. for t in df_tweets['text']])
    X['?'] = np.array([t.count('?') / 1. for t in df_tweets['text']])
    X['"'] = np.array([(t.count('"') + t.count('»')) / 2. for t in df_tweets['text']])

    taille1 = X.shape[0]
    taille2 = X.shape[0]
    
    if 'sentiment' in df_tweets: # si les labels sont fournis
        X['sentiment'] = df_tweets['sentiment']
    else: # sinon
        X['sentiment'] = np.zeros(taille1)

    if drop_dups: # on ne retirera les doublons que pour l'ensemble d'entrainement
        X.drop_duplicates(inplace=True)
        taille2 = X.shape[0]
        print('{} doublons retires.'.format(taille1 - taille2))
        
    print('{} documents vectorises.'.format(taille2))

    return X.drop('sentiment', axis=1), X['sentiment'], voca


def extract_tweets(date_string, days=1, port=27017, limit=0):
    client = pym.MongoClient(port=port)
    collection = client.tweet.tweet
    date_datetime = datetime.strptime(date_string, '%Y-%m-%d')
    date_timestamp = int(timestamp(date_datetime) * 1000)
    date_timestamp += 1000 * 60 * 60 * 24 # on se décale à la fin de la journée en question (23h59)
    window = 1000 * 60 * 60 * 24 * days # fenetre exprimée en millisecondes
    
    fetched_tweets = []
    corpus = collection.find(
        filter={'t_time': {'$gt': (date_timestamp - window), '$lt': date_timestamp}},
        projection={'_id': False, 't_id': 1, 't_text': 1, 't_time': 1}).sort('t_time', pym.DESCENDING).limit(limit)

    count = 0
    for t in corpus:
        count += 1
        fetched_tweets.append({'id': t['t_id'], 'text': t['t_text'], 'timestamp': t['t_time']})

    print('{} tweets trouves.'.format(count))
    client.close()
    result_df = pd.DataFrame(fetched_tweets)
    
    return result_df


def insert_in_mongo(df, port=27017):
    client = pym.MongoClient(port=port)
    collection = client.tweet.predicted
    collection.insert_many(df.to_dict('records'))
    client.close()
