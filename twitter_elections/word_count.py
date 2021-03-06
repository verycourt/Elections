import pymongo as pym
import re
import unicodedata
from nltk import word_tokenize
import string
from collections import Counter 
from nltk.corpus import stopwords

c = pym.MongoClient().tweet.tweet
corpus_valls = c.find({"t_text": re.compile(("valls"), re.I)})
corpus_hamon = c.find({"t_text": re.compile(("hamon"), re.I)})

def normalize_sw(word):
	return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').lower()

french_stopwords = set(stopwords.words('french'))
normalize_french_stop_words = [normalize_sw(i) for i in french_stopwords]


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def count_word(corpus):
	word_list = list()
	nb_tweet = len(corpus)
	for i in range(nb_tweet):

		m_string = unicodedata.normalize('NFKD', corpus[i]["t_text"]).encode('ascii', 'ignore').lower()

		tokens = preprocess(m_string.strip())
	# chargement des stopwords français


	# un petit filtre
		tokens_n = [token for token in tokens if token not in normalize_french_stop_words 
						and token  not in string.punctuation ]
		print("Document " + str(i) + " /" + str(nb_tweet))

		word_list += tokens_n 

	return word_list

corpus_hamon = list(corpus_hamon)
corpus_valls = list(corpus_valls)

word_list_hamon = count_word(corpus_hamon)
word_list_valls = count_word(corpus_valls)

count_hamon = Counter(word_list_hamon)
count_valls = Counter(word_list_valls)

