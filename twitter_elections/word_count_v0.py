#!/usr/bin/python
#coding=latin-1
#export PYTHONWARNINGS="ignore"
import pymongo as pym
import re
import unicodedata
from nltk import word_tokenize
import string
from collections import Counter 
from nltk.corpus import stopwords
import tokenizer 
from stop_words import get_stop_words
from pytagcloud import create_tag_image, make_tags
import time

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

def normalize_sw(word):
	return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').lower()



def tokenize(s):
        regex_str = r"(?:[a-z][a-z'\-_]+[a-z]+\D)"
        tokens_re = re.compile(regex_str, re.VERBOSE | re.IGNORECASE)
	return tokens_re.findall(word_tokenize(s))

def preprocess(s, lowercase=True):
	tokens = tokenizer.tokenize(s)
        if lowercase:
        	tokens = [token.lower() for token in tokens]
    	return tokens

def count_word(corpus):
	stoplists = []
	stop2 = get_stop_words('fr')
	french_stopwords = set(stopwords.words('french'))
	custom_stops = ['rt','hamon','valls','hollande','montebourg','fillon'
	,'macron','le pen','bayrou','pinel','bennhamias','jadot','rugy','sarkozy','melanchon']
	normalize_french_stop_words = [normalize_sw(i) for i in french_stopwords]
	word_list = list()
	nb_tweet = len(corpus)
	for i in range(nb_tweet):
		m_string = unicodedata.normalize('NFKD', corpus[i]["t_text"]).encode('ascii', 'ignore').lower()
		tokens = preprocess(m_string.strip())
		tokens_n = [token for token in tokens if token not in normalize_french_stop_words 
		and token not in string.punctuation and token not in stop2 and token not in custom_stops]
		word_list += tokens_n 
	return word_list

def get_wordcloud(candidate):
	client = pym.MongoClient()
	c = client.tweet.tweet
	removeDuplicates(c)
	words = {}
	words[candidate] = list(c.find({'t_time':{'$lte':now - 3.456e8},"t_text": re.compile((candidate), re.I)},{'t_text':1}))
	client.close()
	words[candidate] = Counter(count_word(words[candidate]))
	TAG_PADDING = 0.05
	ECCENTRICITY = 0.05
	tags = make_tags(words[candidate].most_common(50),minsize=20, maxsize=50)
	create_tag_image(tags,'/var/www/html/decompte/'+candidate+'_cloud.png',layout=2, size=(700,400), fontname='Philosopher')
	f = open('/var/www/html/decompte/listwords'+str(now)+'.txt','a')
	f.write(candidate+' :')
	for word in words[candidate].most_common(50) : f.write(' '+word+' ')
	f.close()

candidates = ['hamon','valls','fillon']
for candidate in candidates :
	get_wordcloud(candidate)
