#!/usr/bin/python
# coding:utf8
import pymongo as pym
import pandas as pd
from sklearn.cluster import KMeans
import re
import gensim
import string
import numpy as np
import json
import wordcloud

def getBagOfWords(text):
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
    for word in text.lower().strip().split():
        word = punctuation.sub('',word.rstrip().lstrip())
        if not re.match(r'^https.*', word) and not re.match('^@.*', word) and not re.match('\s', word) \
        and word not in stopwords : filtered.append(punctuation.sub('',word.rstrip().lstrip()))
    return filtered
  
def getLastTweets(collection):
    lasttweets = [tweet for tweet in collection.find().sort("$natural",-1).limit(200000)]
    exportedTweets = pd.DataFrame(lasttweets)
    exportedTweets.drop(["t_state","_id","t_lat","t_lng","t_RT"], axis =1, inplace="true")
    return exportedTweets

def word2vecTweets(dataframe):
    dataframe["filtered_text"] = dataframe["t_text"].apply(getBagOfWords)
    try :
        model = gensim.models.Word2Vec.load("word2vecmodel")
        model.train([row for row in dataframe["filtered_text"]], min_count=50, size=500)
        model.save("word2vecmodel")
    except :
        model = gensim.models.Word2Vec([row for row in dataframe["filtered_text"]], min_count=50,size=500)
        model.save("word2vecmodel")
    word_vectors = model.syn0
    return word_vectors, model

#def removeFakeTweets():
    #Read blacklist of accounts
    #Remove tweets whose id appears in list
    #Cluster tweets https://github.com/FindKim/Jaccard-K-Means/blob/master/k-means%2B%2B.py

def clusterTweetsTopics(vectors,model):
    clusters = KMeans(n_clusters = vectors.shape[0] / 7 )
    while True:
        try : 
            idx = clusters.fit_predict(vectors) # Perform K-means with clusters of 10 words
            break
        except:
            continue
    wordMap = dict(zip(model.index2word, idx))
    saveAndCloudifyTopics(wordMap)

def saveAndCloudifyTopics(wordMap):
    topics = dict()
    for cluster in range(6): 
        print("Cluster : %d\n" % cluster)
        words = []
        for i in range(len(wordMap.values())):
            if( wordMap.values()[i] == cluster ):
                words.append(wordMap.keys()[i])
        print words
        topics[cluster] = words
        wc = wordcloud.WordCloud(max_font_size = 30, 
        	background_color="white").generate(' '.join(words)).to_file("/var/www/html/decompte/topics/twitter_topic"+str(cluster)+".png")
    file = open("/var/www/html/decompte/topics/topics.json","w")
    json.dump(topics,file)
    file.close()


def main():
    client = pym.MongoClient('localhost',27017)
    tweets = client.tweet.tweet 
    word_vectors,model = word2vecTweets(getLastTweets(tweets)) # Vectorize tweet's text
    															#removeFakeTweets
    clusterTweetsTopics(word_vectors,model) #Extract topics
                                                     # Perform KMeans over quantified columns of tweet to detect clusters
                                                     # Visualise result and determine fake accounts characteristics
main()
