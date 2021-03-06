#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from trendsAPI import * # API non officielle
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import sys
from numpy.random import rand
from numpy import sign
import time


def convert_date_column(dataframe): # Conversion du format en un string court
    dates = []
    rdict = {',': '', ' PST': '', ' à': '', 'janv.': '01', 'févr.': '02', 'mars': '03', 'avr.': '04',
             'mai': '05', 'juin': '06', 'juil.': '07', 'août': '08', 'sept.': '09', 'oct.': '10',
             'nov.': '11', 'déc.': '12'}
    robj = re.compile('|'.join(rdict.keys()))
    
    rdict2 = {' 01 ': ' janv. ', ' 02 ': ' févr. ', ' 03 ': ' mars ', ' 04 ': ' avr. ', ' 05 ': ' mai ',
              ' 06 ': ' juin ', ' 07 ': ' juil. ', ' 08 ': ' août ', ' 09 ': ' sept. ', ' 10 ': ' oct. ',
              ' 11 ': ' nov. ', ' 12 ': ' déc. '}
    robj2 = re.compile('|'.join(rdict2.keys()))
    
    if 'PST' in dataframe['Date'][0]: # format de date anglais avec heure
        in_format = '%b %d %Y %H:%M' # type : Jan 18 2017 12:00
        
        for date in dataframe['Date']: # Conversion en timestamp sur le fuseau GMT+1
            t = datetime.strptime(robj.sub(lambda m: rdict[m.group(0)], date), in_format) + timedelta(hours=9)
            t = datetime.strftime(t, '%d %m %H:%M') # conversion de nouveau en string du type : 18 01 12:00
            dates.append(robj2.sub(lambda m: rdict2[m.group(0)], t)) # remplacement des mois en toutes lettres

    elif 'UTC' in dataframe['Date'][0]: # format de date français avec heure
        in_format = '%d %m %Y %H:%M' # type : 18 01 2017 12:00
        
        for date in dataframe['Date']: # Conversion en timestamp sur le fuseau GMT+1
            t = datetime.strptime(robj.sub(lambda m: rdict[m.group(0)], date[0:-6]), in_format) + timedelta(hours=9)
            t = datetime.strftime(t, '%d %m %H:%M') # conversion de nouveau en string du type : 18 01 12:00
            dates.append(robj2.sub(lambda m: rdict2[m.group(0)], t)) # remplacement des mois en toutes lettres
    
    else: # si les dates ne contiennent pas l'heure (ie. recherche sur plus d'un mois)
        rdict = {', ': ' ', 'janvier': 'janv.', 'février': 'févr.', 'avril': 'avr.', 'juillet': 'juil.',
                 'septembre': 'sept.', 'octobre': 'oct.', 'novembre': 'nov.', 'décembre': 'déc.'}
        robj = re.compile('|'.join(rdict.keys()))
        for date in dataframe['Date']:
            t = robj.sub(lambda m: rdict[m.group(0)], date)
            dates.append(' '.join(t.split(' ')[1:-1]))
    
    dataframe['Date'] = dates
    return


def trends_to_json(queries='candidats_A', periodes='3d'):
    """
    Télécharge sous format json les données de Google Trends avec les paramètres indiqués.
    Ceux-ci doivent appartenir aux recherches préconfigurées dans les dictionnaires <queries>
    et <periodes>.
    
    Si aucun paramètre n'est spécifié, la fonction va balayer toutes les combinaisons de
    requêtes et de périodes préconfigurées.
    """

    # Les termes de recherche (5 au maximum separes par des virgules)
    # On associe a un type de recherche la liste des parametres correspondants
    all_queries = {'candidats_A': '/m/047drb0, /m/04zzm99, /m/02rdgs, /m/011ncr8c, /m/0fqmlm'} 
    all_periodes = {'3d': 'now 3-d', '7d': 'now 7-d'}
    
    queries = set(queries.replace(', ', ',').split(','))
    periodes = set(periodes.replace(', ', ',').split(','))
    
    success = []
    # adresse mail et mot de passe associé
    users = {'pfrlepoint@gmail.com': 'projet_fil_rouge', 'pfrlepoint2@gmail.com': 'pytrends_2'}
    
    for user in list(users.keys())[::int(sign(rand(1) * 2 - 1))]:
        # une chance sur deux de partir de la fin de la liste des adresses gmail
        try:
            # Connection à Google (utiliser une vraie adresse gmail permet plus de requêtes)
            pytrend = TrendReq(user, users[user], custom_useragent='PFR')
            
            for q in queries & set(all_queries): # éléments communs aux deux ensembles
                for p in periodes & set(all_periodes):
                    if (q, p) in success: # si cette requête a déjà été réalisée avec une autre adresse, on itère
                        continue
                    else:
                        payload = {'q': all_queries[q], 'geo': 'FR', 'date': all_periodes[p], 'hl': 'fr-FR'}
                        # Possibilite de periode personnalise : specifier deux dates (ex : 2015-01-01 2015-12-31)
                        # geographie : FR (toute France), FR-A ou B ou C... (region de France par ordre alphabetique)
                        # categorie politique : cat = 396

                        df = pytrend.trend(payload, return_type='dataframe')
                        convert_date_column(df) # converts date into a short string
                        df.set_index('Date', inplace=True)

                        # reduction du nombre de lignes du dataframe a une trentaine de points
                        # pour la lisibilité du graph
                        n = {'4h': 2, '1d': 4, '3d': 1, '7d': 6, '1m': 1, '3m': 2}
                        # n = 1 # pour désactiver cette fonction

                        # Sauvegarde en JSON
                        server_path = '/var/www/html/gtrends/data/' # path complet
                        # server_path = ''
                        df[(df.shape[0] - 1) % n[p]::n[p]].to_json(
                            server_path + q + '_' + p + '.json', orient='split')

                        print('Connexion reussie avec l\'adresse : ' + user)
                        print('Enregistrement sous : ' + server_path + q + '_' + p + '.json')
                        success.append((q, p)) # on garde en mémoire les couples q, p qui ont fonctionné

                        # espacement des requêtes pour ne pas dépasser la limite
                        time.sleep(10)
            return

        except RateLimitError:
            print('Limite de requetes depassee, tentative avec une autre adresse mail...')
            
        except ResponseError:
            print('Connexion bloquee, tentative avec une autre adresse mail...')

    print('Erreur lors de la recuperation des donnees.')
    return


####################################################################
# passage des arguments via sys.argv
if len(sys.argv) == 3:
    trends_to_json(query=sys.argv[1], periode=sys.argv[2])
else:
    trends_to_json()
