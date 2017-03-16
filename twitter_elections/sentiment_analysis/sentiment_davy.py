
# coding: utf-8

# In[1]:

import pymongo as pym
import nltk.data
import re
import string
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import stop_words
from nltk.stem import *
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from scipy.sparse import hstack
from sklearn.linear_model import LogisticRegression



print(stopwords.words('french'))
print('---')
print(stop_words.get_stop_words('fr'))



stops = set(['rt','ds','qd','ss','ns','vs','nn','amp','gt','gd','gds','tt','pr','ac','mm', 'qu',
            '``', 'ni', 'ca', 'le', 'les', ' ', 'si', '$', '^', 'via', 'ils'] +
            list('@ن%£€‘:&;') + list('abcdefghijklmnopqrstuvwxyz'))
print(stops)


def cleanTrainDb():
    client = pym.MongoClient('localhost', 27017)
    collection = client.tweet.train
    textCleanPipeline = [{"$group":{"_id":"$text", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]
    duplicates = []
    try :
        for doc in collection.aggregate(textCleanPipeline) :
            it = iter(doc['dups'])
            next(it)
            for id in it :
                duplicates.append(pym.DeleteOne({'_id':id}))
        c.bulk_write(duplicates)    
    except:
        pass
        client.close()





def tweetPreprocessing(collection, retweet=False):

    tweets = collection.find(filter={'text':{'$exists':True}}, projection={'_id':False})
    #tweets2 = collection2.find(filter={'t_text':{'$exists':True}}, projection={'_id':False})
    
    df = pd.DataFrame()
    listTweets, listCandidats, listSentiments = [], [], []

    for t in tweets: 
        if not retweet: # filtrage des retweets
            if 'rt @' in t['text']:
                continue
        
        # comptes
        a = t['text'].count('!')
        b = t['text'].count('?')
        c = t['text'].count('#')
        d = t['text'].count('"')
        e = t['text'].count('http')
#         if e > 1:
#             e = 1
        
        # mot tronqué
        t['text'] = re.sub(r'\w*…', '', t['text'])
        
        # caracteres speciaux, url et rt
        t['text'] = re.sub(r'\xad', '-',
                           re.sub(r'\n', ' ',
                                  re.sub(r'\W*(?!\S)', '',
                                         re.sub(r'(?:htt)\S*', '',
                                                re.sub(r'^rt.*: ', '',
                                                       re.sub(r'\d', '',
                                                              re.sub(r',;:!?\.\/\*(){}', '',
                                                                     re.sub(r'«»', '', t['text']))))))))
        
        t['text'] = re.sub('|'.join(['’', '_', '-', '\'', '\.', '/', '“', '  ']), ' ', t['text'])
        
        # accents
#         t['text'] = re.sub('|'.join('Ééèêë'), 'e', t['text'])
#         t['text'] = re.sub('|'.join('àâä'), 'a', t['text'])
#         t['text'] = re.sub('|'.join('ç'), 'c', t['text'])
#         t['text'] = re.sub('|'.join('œ'), 'oe', t['text'])
#         t['text'] = re.sub('|'.join('Ôôö'), 'o', t['text'])
#         t['text'] = re.sub('|'.join('îï'), 'i', t['text'])
#         t['text'] = re.sub('|'.join('ùû'), 'u', t['text'])
        
        # apostrophes
        t['text'] = re.sub('|'.join([elem + '\'' for elem in 'cdjlmnst']), '', t['text'])
        
        tokenizer = TreebankWordTokenizer()
        t['text'] = tokenizer.tokenize(t['text'])
        t['text'] = [token for token in t['text'] if (token not in stops) and (len(token)>2)]

        while '' in t['text']:
            t['text'].pop('')
            
        if t['text']: # test si liste non vide
            #listTweets.append(list(set(t['text']))) # mots uniques
            listTweets.append(t['text'])
            try:
                listCandidats.append(t['candidat'])
            except:
                listCandidats.append(None)

            try:
                listSentiments.append(t['sentiment'])
            except:
                listSentiments.append(None)
                
            rec = pd.DataFrame([[a, b, c, d, e]], columns=['!', '?', '#', '"', '_http_'])
            df = df.append(rec, ignore_index=True)
        
    df['text'], df['candidat'], df['sentiment'] = listTweets, listCandidats, listSentiments
    
    return df

def build_feat_mat(df_tweets):
    vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', decode_error='strict',
                                use_idf=True, norm='l2', binary=False, min_df=.0005, max_df=1.)
    X = vectorizer.fit_transform(df_tweets['text'].apply(' '.join))
    hstack((X, df_tweets[['!', '?', '#', '"', '_http_']]))

    return X

def getSentiments(n_predict, retweet) : 
    client = pym.MongoClient('localhost', 27017)
    
    collection = client.tweet.train
    df = tweetPreprocessing(collection, retweet)
    
    collection = client.tweet.labelised
    df2 = tweetPreprocessing(collection, retweet)
    
    df3 = pd.concat([df, df2], axis=0, ignore_index=True)
    df3 = df3.sample(frac=1.0, replace=False) # mélange des lignes
    
    X = build_feat_mat(df3)
    y = df3['sentiment']
    
    n_samples, vocabulaire = X.shape
    print('Tweets : ' + str(n_samples) + ' / ' + 'Mots : ' + str(vocabulaire))
    
    #model = MultinomialNB()
    #model = RandomForestClassifier(n_estimators=30, criterion='gini', max_depth=None, n_jobs=-1)
    #model = KNeighborsClassifier(n_neighbors=15, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', n_jobs=-1)
    model = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, class_weight='balanced')
    
    model.fit(X[:-n_predict], y[:-n_predict])
    predictions = model.predict(X[n_samples - n_predict:])
    
    print('Score', np.sum(predictions == y[n_samples - n_predict:]) / len(predictions))
    return predictions



cleanTrainDb()
client = pym.MongoClient('localhost', 27017)
collection = client.tweet.labelised

corpus = tweetPreprocessing(collection, retweet=True)
print('Taille base d\'entrainement :', corpus.shape[0])
print(corpus['sentiment'].value_counts())


corpus[:10]


a = getSentiments(800, retweet=True)
print(len(a[a==1]), len(a[a==0]))


# calculer des f-score, sentiwordnet, bigrammes...

