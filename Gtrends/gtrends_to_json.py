#!/usr/bin/python
# coding: utf-8

from pytrends.request import TrendReq
import sys
import pandas as pd
from datetime import timedelta
from numpy.random import rand
from numpy import sign

def trends_to_json(queries='candidats_A', periodes='7d'):
    """
    Télécharge sous format json les données de Google Trends avec les paramètres indiqués.
    Ceux-ci doivent appartenir aux recherches préconfigurées dans les dictionnaires
    <all_queries> et <all_periodes>.
    
    Il est possible d'indiquer plusieurs périodes et requetes en les séparant par des virgules.
    """

    # TODO: compléter les dictionnaires de requetes et périodes possibles
    # Les termes de recherche (5 au maximum dans une liste)
    all_queries = {'candidats_A': ['/m/0fqmlm', '/m/0551nw', '/m/02rdgs', '/m/011ncr8c', '/m/04zzm99']}
    all_periodes = {'1h': 'now 1-H', '4h': 'now 4-H', '1d': 'now 1-d', '7d': 'now 7-d', '1m': 'today 1-m'}
    
    trad = {'/m/061czc': 'Michèle Alliot-Marie', '/m/0h3t838': 'Nathalie Artaud', '/m/02y2cb': 'François Bayrou',
            '/m/047fzn': 'Jacques Cheminade', '/m/0f6b18': 'Nicolas Dupont-Aignan', '/m/0fqmlm': 'François Fillon',
            '/m/0551nw': 'Benoît Hamon', '/m/05zztc0': 'Yannick Jadot', '/m/02rdgs': 'Marine Le Pen',
            '/m/011ncr8c': 'Emmanuel Macron', '/m/04zzm99': 'Jean-Luc Mélanchon', '/m/0gxyxxy': 'Philippe Poutou',
            '/m/047drb0': 'Manuel Valls'}
    
    queries, periodes = set(queries.replace(', ', ',').split(',')), set(periodes.replace(', ', ',').split(','))
    
    success = []
    # adresse mail et mot de passe associé
    users = {'pfrlepoint@gmail.com': 'projet_fil_rouge', 'pfrlepoint2@gmail.com': 'pytrends_2'}
    
    # une chance sur deux de partir de la fin de la liste des adresses gmail
    for user in list(users.keys())[::int(sign(rand(1) * 2 - 1))]:
        
        try:
            # Login to Google. Only need to run this once, the rest of requests will use the same session.
            pytrend = TrendReq(user, users[user], custom_useragent='My Pytrends Script')
            
            for q in queries & set(all_queries): # éléments communs aux deux ensembles
                for p in periodes & set(all_periodes): # les requetes et periodes non valides seront ignorées
                    
                    if (q, p) in success: # si cette requête a déjà été réalisée avec une autre adresse, on itère
                        continue
                    else:
                        # categorie politique : cat = 396
                        # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
                        pytrend.build_payload(kw_list=all_queries[q], timeframe=all_periodes[p], cat=0, geo='FR')
                        
                        df = pytrend.interest_over_time()
                        df.rename(columns=trad, inplace=True) # Nom des champs de recherche en colonne
                        
                        if p in ['1h', '4h', '1d', '7d']: # lorsque la fenetre de temps renvoie un format heure...
                            df.index = [date + timedelta(hours=1) for date in df.index] # on convertit les dates en GMT+1

                        # reduction du nombre de lignes du dataframe a une trentaine de points
                        # pour la lisibilité du graph
                        n = {'1h': 2, '4h': 5, '1d': 5, '3d': 1, '7d': 6, '1m': 1, '3m': 2}
                        # n = 1 # pour désactiver cette fonction
                        
                        # TODO: automatiser le n en calculant automatiquement le ratio qui convient
                        # pour obtenir une trentaine de points

                        # Sauvegarde en JSON
                        server_path = '/var/www/html/gtrends/data/' # path complet AWS
                        # server_path = ''
                        df[(df.shape[0] - 1) % n[p]::n[p]].to_json(
                            server_path + q + '_' + p + '.json', orient='split')

                        print('Connexion réussie avec l\'adresse : ' + user)
                        print('Enregistrement sous : ' + server_path + q + '_' + p + '.json')
                        success.append((q, p)) # on garde en mémoire les couples q, p qui ont fonctionné

                        # espacement des requêtes pour ne pas dépasser la limite
                        # time.sleep(10)
            return

        except:
            pass

    print('Erreur lors de la recuperation des donnees.')
    return


####################################################################
# passage des arguments via sys.argv
if len(sys.argv) == 3:
    trends_to_json(queries=sys.argv[1], periodes=sys.argv[2])
else:
    trends_to_json()
