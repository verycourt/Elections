#!/usr/bin/python
# coding: utf-8

from datetime import date, datetime, timedelta
from predict_functions import *
from sklearn.externals import joblib
import pandas as pd
import pymongo as pym
import re


date = datetime.strftime(datetime.utcnow() - timedelta(hours=24), '%Y-%m-%d')
fname = 'data/twitter_sentiments_{}.json'.format(date)

df_pred = pd.DataFrame()

# 1. Chargement du vocabulaire
voca = pd.read_json('trained_dict.json').to_dict()[0]

# 2. Chargement des tweets a predire
# dataframe contenant les tweets a predire dans une colonne 'text'
print('Chargement des tweets des candidats depuis la base MongoDB ...')
df = extract_tweets(date, days=1, port=27017)

other_politicians = ['bayrou', 'aignan', 'poutou', 'arthaud', 'cheminade', 'valls', 'sarko', 'hollande']
candidates = {'macron': 'macron|emmanuel',
              'fillon': 'fillon',
              'hamon': 'hamon|benoit|benoît',
              'melenchon': 'melenchon|mélenchon|jlm',
              'le pen': 'le pen|lepen|mlp|marine'
             }

# on repère les tweets où plusieurs candidats sont cités
stop_words = '|'.join([pol for pol in other_politicians])
df['other'] = df['text'].str.contains(stop_words, case=False) 

# on repère les candidats contenus dans les tweets
for candidate in candidates:
    df[candidate] = df['text'].str.contains(candidate, case=False)
    
# filtrage des tweets contenant d'autres personnalités politiques
df = df[df['other']==False]

# filtrage des tweets contenant plusieurs des 5 candidats (ou aucun candidat)
df['count'] = 1 * df.fillon + df.macron + df['le pen'] + df.melenchon + df.hamon
df = df[df['count']==1]
df.reset_index(drop=True, inplace=True)

# 3. Creation des features et de la matrice TF-IDF pour la base test
X_test, _, _ = build_Xy(df, drop_dups=False, vocab=voca, min_df=3, n_grams=(1,1))

# 4. Chargement du modele entraine
clf = joblib.load('trained_logistic_regression.pkl')

# 5. Prediction
print('Prediction des tweets...')
y_pred = clf.predict(X_test)
df['sentiment'] = y_pred

# 6. Sauvegarder les predictions
# ajout de la ligne du candidat dans le dataframe
for candidate in candidates:
    curr_df = df[df[candidate]==True]
    taille = curr_df.shape[0]
    rec = {'count': taille, 'candidat': candidate}
    try:
        rec['neg'] = curr_df[curr_df['sentiment']==-1].shape[0] / taille
        rec['neu'] = curr_df[curr_df['sentiment']==0].shape[0] / taille
        rec['pos'] = curr_df[curr_df['sentiment']==1].shape[0] / taille
    except:
        # si aucun tweet pour le candidat courant n'est dans la base
        rec['neg'], rec['neu'], rec['pos'] = ('-', '-', '-')
    
    df_pred = df_pred.append(rec, verify_integrity=False, ignore_index=True)
df_pred.set_index('candidat', drop=True, inplace=True)

print('Sauvegarde des pourcentages par candidat dans un .json : {}'.format(fname))
print(df_pred)
df_pred.to_json(fname)

print('Insertion dans la base MongoDB "predicted"...')
insert_in_mongo(df.drop(['other', 'count'], axis=1), port=27017)