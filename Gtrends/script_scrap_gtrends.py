#!/usr/bin/python
# coding: utf-8

from trendsAPI import TrendReq # API non officielle
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import sys


# Formattage de la date pour gérer le format heure:minute
def convert_date_column(dataframe, out='%d/%m %H:%M'):
	dates = []
	if 'PST' in dataframe['Date'][0]:  # format de date anglais
		rdict = {',': '', ' PST': ''}
		in_format = '%b %d %Y %H:%M'  # ex: Jan 18 2017 12:00
		out_format = out  # ex: 18/01 12:00
	elif 'UTC−8' in dataframe['Date'][0]:  # format de date français
		rdict = {' à': '', ' UTC−8': '', 'janv.': '01', 'févr.': '02', 'mars': '03', 'avr.': '04', 
		'mai': '05', 'juin': '06', 'juil.': '07', 'août': '08', 'sept.': '09', 'oct.': '10', 
		'nov.': '11', 'déc.': '12'}
		in_format = '%d %m %Y %H:%M'  # ex: 18 01 2017 12:00
		out_format = out  # ex: 18/01 12:00

	else:  # si les dates ne contiennent pas l'heure,
		return

	robj = re.compile('|'.join(rdict.keys()))
	for date in dataframe['Date']:  # Conversion des dates
		t = datetime.strptime(robj.sub(lambda m: rdict[m.group(0)], date), in_format) + timedelta(hours=9)  # GMT+1
		dates.append(datetime.strftime(t, out_format))

	dataframe['Date'] = dates
	return


def trends_to_json(query='candidats_majeurs', periode='3d'):
	# Formats possibles pour la date : now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m
	periodes = {'1h': 'now 1-H', '4h': 'now 4-H', '1d': 'now 1-d', '3d': 'now 3-d', 
	'7d': 'now 7-d', '1m': 'today 1-m', '3m': 'today 3-m'}

	# Les termes de recherche (5 au maximum separes par des virgules)
	# On associe a un type de recherche la liste des parametres correspondants
	queries = {'candidats_majeurs': '/m/047drb0, /m/05zztc0, /m/02rdgs, /m/011ncr8c, /m/0fqmlm', 
	'partis_majeurs': '/g/11b7n_r2jq, /m/01qdcv, /m/0hp7g, /m/0h7nzzw', 
	'divers_gauche': 'france insoumise, /m/01vvcv, /m/04glk_t, /m/01v8x4'} 
	# se referer a la table de correspondance ci-dessus

	if (query not in queries) or (periode not in periodes):
		print('Erreur de parametre')
		return

	users = ['pfrlepoint@gmail.com', 'pfrlepoint2@gmail.com']
	for user in users:
		try:
			# Connection to Google (use a valid Google account name for increased query limits)
			pytrend = TrendReq(user, 'projet_fil_rouge', custom_useragent='pfr')

			# Possibilite de periode personnalise : specifier deux dates (ex : 2015-01-01 2015-12-31)

			# geographie : FR (toute France), FR-A ou B ou C... (region de France par ordre alphabetique)
			# categorie politique : cat = 396

			# On fait la requete sur Google avec les parametres choisis
			payload = {'q': queries[query], 'geo': 'FR', 'date': periodes[periode]}
			df = pytrend.trend(payload, return_type='dataframe')

			if periode[-1] != 'm':
				convert_date_column(df, out='%d/%m %H:%M')  # converts into a standard date format like: 18/01 12:00
				#         else:
				#             df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
				#             dates = []
				#             for elem in df['Date']:
				#                 dates.append(datetime.strftime(elem, '%d/%m'))
				#             df['Date'] = dates

			df.set_index('Date', inplace=True)

			# reduction du nombre de lignes du dataframe par un facteur n pour la lisibilité du graph
			# (on laisse une trentaine de lignes)
			n = {'1h': 2, '4h': 1, '1d': 3, '3d': 2, '7d': 6, '1m': 1, '3m': 3}

			print('Connexion à Google réussie avec le compte ' + user)
			# chemin sur le serveur AWS
			path_AWS = '/var/www/html/Gtrends/data/'

			# Sauvegarde en JSON
			df[(df.shape[0] - 1) % n[periode]::n[periode]].to_json(
				path_AWS + query + '_' + periode + '.json', orient='split')
			print('Sauvegarde dans : ' + query + '_' + periode + '.json')
			return

		except:
			continue

	print('Un problème est survenu, les données ne sont pas sauvegardées.')
	return

####################################################################
# passage des arguments via sys.argv
if len(sys.argv) != 3:
	print('Il faut passer deux arguments en paramètre : cf le fichier readme.')
else:
	trends_to_json(query=sys.argv[1], periode=sys.argv[2])