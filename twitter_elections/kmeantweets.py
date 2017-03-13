import pymongo as pym
import pandas as pd
from sklearn.cluster import KMeans
import re
import gensim

def removeStopWords(text):
    stopwords = [u"rt",u"alors",u"aucuns",u"aussi",u"autre",u"avant",u"avec",u"avoir",u"bon",u"car",u"ce",u"cela",u"ces",
    u"ceux",u"chaque",u"ci",u"comme",u"comment",u"dans",u"de",u"des",u"d",u"dedans",u"dehors",u"depuis",u"devrait",u"doit",u"donc",
    u"dos",u"début",u"elle",u"elles",u"en",u"encore",u"essai",u"est",u"et",u"e",u"fait",u"faites",u"fois",u"font",u"hors",u"ici",
    u"il",u"ils",u"je",u"juste",u"la",u"le",u"les",u"leur",u"là",u"ma",u"maintenant",u"mais",u"mes",u"mine",u"moins",u"mon",u"mot",
    u"même",u"ni",u"nommés",u"notre",u"nous",u"o",u"où",u"par",u"parce",u"pas",u"peut",u"pe",u"plupart",u"pour",u"pourquoi",u"quand",
    u"que",u"quel",u"quelle",u"quelles",u"quels",u"qui",u"sa",u"sans",u"ses",u"seulement",u"si",u"sien",u"son",u"sont",u"sous",u"soyez",
    u"sujet",u"sur",u"ta",u"tandis",u"tellement",u"tels",u"tes",u"ton",u"tous",u"tout",u"trop",u"très",u"t",u"voient",u"vont",u"votre",
    u"vous",u"v",u"ça",u"étaient",u"état",u"étions",u"été",u"être",u"or",u"c'",u"se",u"ses",u"sa",u"ce",u"ces",u"ca",u"s'",u"l'",u"qu'",
    u"a",u"à",u"avais",u"étais",u"d'",u"qui",u"quoi",u"q",u"ont",u"as",u"avait",u"avaient",u"avez",u"étaient",u"était",u"étiez",u"y",
    u"leurs",u"leur",u"t",u"m",u"https",u"co",u"sera",u"aura",u"seraient",u"serais",u"auraient",u"un",u"une",u"le",u"les",u"la",u"&gt"]
    filtered = [word for word in text.lower().split() if word not in stopwords]
    return filtered
  
def getLastTweets(collection):
    lasttweets = [tweet for tweet in collection.find().sort("$natural",-1).limit(250000)]
    exportedTweets = pd.DataFrame(lasttweets)
    exportedTweets.drop(["t_state","_id","t_lat","t_lng","t_RT"], axis =1, inplace="true")
    return exportedTweets

def word2vecTweets(dataframe):
    dataframe["filtered_text"] = dataframe["t_text"].apply(removeStopWords)
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
    #Cluster tweets

def clusterTweetsTopics(vectors,model):
    clusters = KMeans(n_clusters = vectors.shape[0] / 5 )
    idx = cluster.fit_predict(vectors) # Perform K-means with clusters of 5 words
    wordMap = dict(zip(model.index2word, idx))
    displayClusterOfWords(wordMap)

def displayClusterOfWords(wordMap):
    for cluster in range(6): 
        print("Cluster : %d\n" % cluster)
        words = []
        for i in range(len(wordmap.values())):
            if( wordMap.values()[i] == cluster ):
                words.append(wordMap.keys()[i])
        print words

def main():
    client = pym.MongoClient('localhost',27017)
    tweets = client.tweet.tweet
                                #removeFakeTweets
    word_vectors,model = word2vecTweets(getLastTweets(tweets)) # Vectorize tweet's text
    clusterTweetsTopics(word_vectors,model)
                                                     # Perform KMeans over quantified columns of tweet to detect clusters
                                                     # Visualise result and determine fake accounts characteristics
                                                     # perfom LDA to view main topics on twitter
    #kmeans = KMeans(n_init=10, init="k-means++", verbose=1, n_clusters=10).fit(exportedTweets)       
    
main()