#!/usr/bin/python
#coding=utf-8
#export PYTHONWARNINGS="ignore"
import pymongo as pym
import re
import string
from collections import Counter 
import time
import pandas as pd
import wordcloud
now = time.time()*1000

def removeDuplicates(c):
	duplicates = []
	removepipe = [{"$group":{"_id":"$t_id", "dups":{"$push":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}]
	try :
		for doc in c.aggregate(removepipe) :
			it = iter(doc['dups'])
			next(it)
			for id in it :
				duplicates.append(pym.DeleteOne({'_id':id}))
		c.bulk_write(duplicates)	
	except:
		pass

def preprocess(text):
    stopwords = [u"enculé",u"bite",u"chatte",u"cul",u"con",u"connard", u"rt",u"alors",u"aucuns",u"pute",u"salope",
    u"aussi",u"autre",u"avant",u"avec",u"avoir",u"bon",u"car",u"ce",u"cela",u"ces",u"&amp",u"gtgt"
    u"ceux",u"chaque",u"ci",u"comme",u"comment",u"dans",u"de",u"des",u"d",u"dedans",u"dehors",u"depuis",u"devrait",u"doit",u"donc",
    u"dos",u"début",u"elle",u"elles",u"en",u"encore",u"essai",u"est",u"et",u"e",u"fait",u"faites",u"fois",u"font",u"hors",u"ici",
    u"il",u"ils",u"je",u"juste",u"la",u"le",u"les",u"leur",u"là",u"ma",u"maintenant",u"mais",u"mes",u"mine",u"moins",u"mon",u"mot",
    u"même",u"ni",u"nommés",u"notre",u"nous",u"o",u"où",u"par",u"parce",u"pas",u"peut",u"pe",u"plupart",u"pour",u"pourquoi",u"quand",
    u"que",u"quel",u"quelle",u"quelles",u"quels",u"qui",u"sa",u"sans",u"ses",u"seulement",u"si",u"sien",u"son",u"sont",u"sous",u"soyez",
    u"sujet",u"sur",u"ta",u"tandis",u"tellement",u"tels",u"tes",u"ton",u"tous",u"tout",u"trop",u"très",u"t",u"voient",u"vont",u"votre",
    u"vous",u"v",u"ça",u"étaient",u"état",u"étions",u"été",u"être",u"or",u"c'",u"se",u"ses",u"sa",u"ce",u"ces",u"ca",u"s'",u"l'",u"qu'",
    u"a",u"à",u"avais",u"étais",u"d'",u"qui",u"quoi",u"q",u"ont",u"as",u"avait",u"avaient",u"avez",u"étaient",u"était",u"étiez",u"y",
    u"leurs",u"leur",u"t",u"m",u"https",u"co",u"sera",u"aura",u"seraient",u"serais",u"auraient",u"un",u"une",u"le",u"les",u"la",u"&gt"]
    filtered = []
    punctuation = re.compile('[%s]' % re.escape('!"%&()*+-=,.:/;<>[\]^_`{|}~...'))
    for word in text:
        word = punctuation.sub('',word.lower().rstrip().lstrip())
        if not re.match(r'^https.*', word) and not re.match('^@.*', word) and not re.match('\s', word) \
        and word not in stopwords : filtered.append(punctuation.sub('',word.rstrip().lstrip()))
    return filtered

def get_wordcloud(candidate):
	client = pym.MongoClient()
	c = client.tweet.tweet
#	removeDuplicates(c)
	words = {}
	df = pd.DataFrame([tweet for tweet in c.find({'t_time':{'$lte':now - 3.456e8},"t_text": re.compile((candidate), re.I)},
        {'t_text':1}).limit(100)])
	client.close()
	words[candidate] = Counter(preprocess(df['t_text']))
        wc = wordcloud.WordCloud(max_font_size = 30, background_color="white").generate(' '.join(words[candidate])).to_file("/var/www/html/decompte/cloud_"+candidate+".png")
candidates = ['hamon','macron','fillon','Le Pen','mélenchon']
for candidate in candidates :
	get_wordcloud(candidate)
