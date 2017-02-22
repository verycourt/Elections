import pymongo as pym
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from collections import Counter
import time
import numpy as np
import tweepy
from sklearn import mixture

def removeDuplicates():
    client = pym.MongoClient()
    c = client.tweet.tweet
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
    client.close()


def timeConverter(date):
    now = time.time() / (3600 * 24)
    timestamped = time.mktime(time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')) / (3600 * 24)
    offset = now - timestamped
    return offset

def getUsers(collection):
    lasttweets = pd.DataFrame([tweet for tweet in collection.find({},{"t_user":1}).sort("$natural",-1).limit(100000)])
    users = dict(lasttweets['t_user'])
    DF = pd.DataFrame(users).T
    cleanDF = DF[['default_profile','default_profile_image',
    'favourites_count','followers_count','friends_count','listed_count','statuses_count','verified','created_at']]
    cleanDF['created_at'] = cleanDF['created_at'].map(lambda x : timeConverter(x))
    ids = DF['id']
    return cleanDF, ids

def kmeansClustering(users, ids, api):
    kmeans = KMeans(n_clusters=100, verbose=0).fit(users)
    cnt = Counter(kmeans.labels_)
    for i,c in enumerate(kmeans.cluster_centers_):
        print("Centre du cluster : ","Followers / Following : %.1f |" %(c[3]/c[4]), "tweets / days : %d | " %(c[6]/c[8]), "count %d" %cnt[i])
        for p in ids[np.where(kmeans.labels_ == i)[0][:3]] :
            try :
                profile = api.get_user(p)
                print("Profils du cluster\n", "Followers : ", profile.followers_count, "\n","Friends : ", 
                profile.friends_count, "\n", "Verified : ", profile.verified, "\n",
                "tweets : ", profile.statuses_count, "\n","Location : ", profile.location, "\n",
                "Date Création : ", profile.created_at, "\n","URL : https://twitter.com/intent/user?user_id="+str(p))
            except : continue


def mixtureClustering(data, indexes) :
    gmm = mixture.GaussianMixture(n_components=5, covariance_type='full').fit(data)
    print("Weights : ", gmm.weights_, "\n", "means : ", gmm.means_, "\n","Covariances : ", gmm.covariances_,"\n")

def main():
    auth = tweepy.OAuthHandler("38wnscCtD7hDZwGX4slpNAACW", "BxZ3HF9km43U14qYkcX3vxxpXUeFiWQppPHhWDgsaVDOcPkPUD")
    auth.set_access_token("334722973-NY6Dm1sQn8pHAlNMQhkn6L7uP4rYngY1qqCvBpmt", "Qp8aiuHCzDGudIGeD29TZ99bOOn3wYQXAPSCnAblyCIeS")
    api = tweepy.API(auth)
    client = pym.MongoClient('localhost',27017)
    users, ids = getUsers(client.tweet.tweet)
    client.close()
    kmeansClustering(users, ids, api)
    mixtureClustering(users, ids)

removeDuplicates()
main()