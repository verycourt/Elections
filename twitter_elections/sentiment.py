import pymongo as pym
import nltk.data
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import stop_words
from nltk.stem import *
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
import numpy as np


client = pym.MongoClient('localhost',27018)
collection = client.tweet.cleaned
tokenizer = TreebankWordTokenizer()
stops = set(stopwords.words('french')+stop_words.get_stop_words('fr')+['rt','ds','qd','ss','ns','vs','nn','amp','gt','gd','gds','tt','pr','ac','mm'])

def getCleanTweetsByCandidates(collection, candidat):
    tweets = collection.find({'candidat':candidat},{'_id':False})
    listTweets = []
    for t in tweets : 
        t['text'] = re.sub(r'\w*…','',t['text'])
        t['text'] = re.sub(r',;:!?\.\/\*``"#@(){}','',re.sub(r'\xad','-',re.sub(r'\n',
            ' ',re.sub(r'\W*(?!\S)','',re.sub(r'(?:htt)\S*','',re.sub(r'^rt.*: ','',string=t['text']))))))
        t['text'] = tokenizer.tokenize(t['text'])
        t['text'] = [re.sub(r'[^a-zA-Z0-9-éèêàâùçîœ’\']+','',token,re.UNICODE) for token in t['text'] if token not in stops]
        t['text'] = [re.sub(r'l\'|\squ\'|l’|\squ’|d\'|d’','',token) for token in t['text']]
        while '' in t['text'] : t['text'].remove('')
        listTweets.append(t)
    return listTweets

def vectorize(tokenizedCorpus):
    vectorizer = TfidfVectorizer(max_df = 0.8, min_df=0.0005)
    X = vectorizer.fit_transform(tokenizedCorpus)
    return X

def getSentiments(candidat) : 
    df = pd.DataFrame(getCleanTweetsByCandidates(collection, 'macron'))
    tfidfmat = vectorize(df['text'].apply(' '.join))
    print(tfidfmat.shape)
    nb = MultinomialNB()
    nb.fit(tfidfmat[::2], df.ix[::2,'sentiment'])
    predictions = nb.predict(tfidfmat[1::2])
    accuracy = np.sum(predictions != df.ix[1::2,'sentiment']) / len(df.ix[1::2,'sentiment'])
    print("accuracy of the sklearn naive bayes : ", accuracy)
