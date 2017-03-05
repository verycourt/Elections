#!/usr/bin/python
# coding: utf-8

import sys
import requests
from datetime import date, datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
if sys.version_info[0] == 2:
    import urllib2 as ul # Python2
else:
    import urllib.request as ul # Python3
import json


def FacebookPageData(page_id, access_token):
    
    # construct the URL string
    base = 'https://graph.facebook.com/v2.8'
    node = '/' + page_id
    parameters = '/?access_token=%s&fields=name,talking_about_count,fan_count' % access_token
    url = base + node + parameters
    
    # retrieve data
    response = ul.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    print('Facebook page :', data['name'])
    return [int(data[metric]) for metric in ['fan_count', 'talking_about_count']]

def YoutubePageData(page_id, access_token):
    base = 'https://www.googleapis.com/youtube/v3/channels'
    parameters = '?part=statistics&id=' + page_id + '&key=' + access_token
    url = base + parameters
    
    # retrieve data
    response = ul.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    statistics = data['items'][0]['statistics']

    return [int(statistics[metric]) for metric in ['subscriberCount', 'viewCount', 'videoCount']]

def YoutubeVideosData(page_id, access_token):
    base = 'https://www.googleapis.com/youtube/v3/search'
    parameters = '?order=date&part=snippet&channelId=' + page_id + '&maxResults=10&key=' + access_token
    url = base + parameters
    
    # retrieve list of the most recently published videos on the channel (10 or less)
    response = ul.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    videoIds = [e['id']['videoId'] for e in data['items'] if 'videoId' in e['id']]
    
    base = 'https://www.googleapis.com/youtube/v3/videos'
    parameters = '?part=statistics&id=' + ','.join(videoIds) + '&key=' + access_token
    url = base + parameters
    
    response = ul.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    keys = data['items'][0]['statistics'].keys() # list of metrics
    n = len(data['items'])
    
    # Construction du dictionnaire des valeurs moyennes pour chaque clé sur les vidéos analysées
    videoStats = {key: int(round(sum([int(e['statistics'][key]) for e in data['items']]) / n)) for key in keys}
    
    print('Getting average metrics for the latest', n, 'videos of the channel')

    return [videoStats[metric] for metric in ['viewCount', 'likeCount', 'dislikeCount']]


# {Candidat : [Chaine Youtube, Compte Facebook, Compte Twitter]}
accounts = {#'Alliot-Marie': [None, 'MAlliotMarie', 'MAlliotMarie'],
           #'Arthaud': ['UCZsh-MrJftAOP_-ZgRgLScw', 'nathaliearthaud', 'n_arthaud'],
           #'Bayrou': [None, 'bayrou', 'bayrou'],
           #'Cheminade': ['UCCPw8MX-JcsiTzItY-qq1Fg', 'Jcheminade', 'Jcheminade'],
           #'Dupont-Aignan': ['UCfA5DnCDX3Ixy5QOAMGtBlA', 'nicolasdupontaignan', 'dupontaignan'],
           'Fillon': ['UCp1R4BFJrKw34PfUc3GDLkw', 'FrancoisFillon', 'francoisfillon'],
           'Hamon': ['UCcMryUp6ME3BvP2alkS1dKg', 'hamonbenoit', 'benoithamon'],
           #'Jadot': ['UCsUMhb2ygeTSS2mXLTIDHMQ', 'yannick.jadot', 'yjadot'],
           'Le Pen': ['UCU3z3px1_RCqYBwrs8LJVWg', 'MarineLePen', 'MLP_officiel'],
           'Macron': ['UCJw8np695wqWOaKVhFjkRyg', 'EmmanuelMacron', 'emmanuelmacron'],
           'Melenchon': ['UCk-_PEY3iC6DIGJKuoEe9bw', 'JLMelenchon', 'JLMelenchon'],
           'Poutou': [None, 'poutou.philippe', 'PhilippePoutou']}

app_id = "615202351999343"
app_secret = "ea787efd843d1de746817ec6e9bf7e94"
access_token = app_id + "|" + app_secret
google_key = 'AIzaSyBkRrj_kFDUv-T76CJaI3Pd-g3v7UY4GMA'

today = (datetime.utcnow() + timedelta(hours=1)).date()
fname = str(today) + '.json'
# path = 'data/' # save path
path = '/var/www/html/duel/data/'

df = pd.DataFrame()
print('Maj du', today)

for candidate in accounts:
    print('-' * 20)
    print(candidate)
    print('-' * 20)

    stats = {}
    try: # Twitter : [tweets, followers]
        print('Analyzing Twitter account', accounts[candidate][2])
        soup = BeautifulSoup(requests.get('https://twitter.com/' + accounts[candidate][2] + '?lang=en').text, 'lxml')
        stats_tw = [int(tag.attrs['title'].replace(',', '').split(' ')[0])
                    for tag in soup.find_all(class_='ProfileNav-stat', limit=3) if 'title' in tag.attrs]
    except:
        stats_tw = ['-', '-', '-']
        print('Profil Twitter : une erreur est survenue...')

    _, _, stats['0_tw_followers'] = stats_tw

    if accounts[candidate][0] is not None:
        print('Scanning Youtube Channel')
        try: # Youtube [abonnés, total vues, nombre de vidéos]
            stats_yt = YoutubePageData(accounts[candidate][0], google_key)
        except:
            stats_yt = ['-', '-', '-']
            print('Page Youtube : une erreur est survenue...')
        try: # Youtube [moyenne vues 10 vidéos, moyenne likes 10 vidéos, moyenne dislikes 10 vidéos]
            stats_yt2 = YoutubeVideosData(accounts[candidate][0], google_key)
        except:
            stats_yt2 = ['-', '-', '-']
            print('Vidéos Youtube : une erreur est survenue...')
    else:
        print('No Youtube Channel')
        stats_yt, stats_yt2 = ['-', '-', '-'], ['-', '-', '-']

    stats['2_yt_subscribers'], _, _ = stats_yt
    stats['3_yt_views_avg'], _, _ = stats_yt2
    
    try:
        stats['4_yt_reaction_rate'] = round((float(stats_yt2[1] + stats_yt2[2]) / stats_yt2[0]) * 100, 1)
        stats['5_yt_satisfaction_rate'] = round((float(stats_yt2[1]) / (stats_yt2[2] + stats_yt2[1])) * 100, 1)
    except:
        stats['4_yt_reaction_rate'] = '-'
        stats['5_yt_satisfaction_rate'] = '-'
    
    try: # Facebook : [likes, people talking about this]
        stats_fb = FacebookPageData(accounts[candidate][1], access_token)
    except:
        stats_fb = ['-', '-']
        print('Page Facebook : une erreur est survenue...')

    stats['6_fb_likes'], stats['7_fb_talking_about'] = stats_fb

    print()
    print(stats)
    
    # ajout de la ligne du candidat dans le dataframe
    rec = pd.DataFrame([stats.values()], columns=stats.keys(), index=[candidate])
    df = df.append(rec, verify_integrity=False)

# ajout de la colonne des mentions twitter sur 3 jours
b = pd.read_json('/var/www/html/decompte/popcontest.json', orient='column')
names, counts = [e['name'] for e in b['children']], [e['size'] for e in b['children']]
names = [n.replace('MLP', 'Le Pen') for n in names]

b = pd.DataFrame(counts, columns=['1_tw_mentions'], index=names)
c = pd.concat([df,b], axis=1, join_axes=[df.index])

df_final = c.sort_index(axis=0).sort_index(axis=1)
df_final.fillna(value='-', inplace=True)

# Sauvegarde des données depuis le dataFrame vers le fichier JSON
df_final.to_json(path + fname, orient='split')
df_final.to_json(path + 'radar.json', orient='split')

print('Data saved as ' + path + fname)