import treetaggerwrapper
import pymongo as pym
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np


def process_texts(list_of_texts, pos_tag_list, stop_words):
    # Processing the tweets (POS tagging, lemmatization, spellchecking)
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
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
    # Tweet feature extraction
    hashtag = np.array([t.count('#') / 2. for t in df_tweets['text']])
    links = np.array([(t.count('http') / 2.) if t.count('http') > 1 else 0 for t in df_tweets['text']])
    at = np.array([t.count('@') / 1. for t in df_tweets['text']])
    n_car = np.array([np.log(len(t))/4 / 1. for t in df_tweets['text']])
    n_words = np.array([np.log(len(t.split(' '))) / 2 for t in df_tweets['text']])
    n_2points = np.array([t.count(':') / 1. for t in df_tweets['text']])
    n_exc = np.array([t.count('!') / 1. for t in df_tweets['text']])
    n_int = np.array([t.count('?') / 1. for t in df_tweets['text']])
    n_quotes = np.array([(t.count('"') + t.count('»')) / 2. for t in df_tweets['text']])

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
    print('Longueur du vocabulaire : {}'.format(len(vectorizer.vocabulary_)))
    X = pd.DataFrame(mat.toarray())
    X_added_features = pd.DataFrame(data={'#': hashtag,
                                          'http': links,
                                          '@': at,
                                          'n_car': n_car,
                                          'n_words': n_words,
                                          ':': n_2points,
                                          '!': n_exc,
                                          '?': n_int,
                                          '""': n_quotes
                                         })
    X = pd.concat([X, X_added_features], axis=1)
    taille1 = X.shape[0]
    taille2 = X.shape[0]
    
    if 'sentiment' in df_tweets: # si les labels sont fournis
        X = pd.concat([X, df_tweets['sentiment']], axis=1)
    else: # sinon
        X['sentiment'] = np.zeros(taille1)

    if drop_dups: # on ne retirera les doublons que pour l'ensemble d'entrainement
        X.drop_duplicates(inplace=True)
        taille2 = X.shape[0]
        print('{} doublons retires.'.format(taille1 - taille2))
        
    print('{} documents vectorises.'.format(taille2))

    return X.drop('sentiment', axis=1), X['sentiment'], vectorizer.vocabulary_