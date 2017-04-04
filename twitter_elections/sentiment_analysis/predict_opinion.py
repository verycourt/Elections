import pymongo as pym
import time
import pandas as pd
import pickle
import re
import numpy as np
import JSON

def extractTweets(port=27018):
    client = pym.MongoClient(port=port)
    now = time.time() * 1000
    collection = client.tweet.tweet
    candidats = ['macron','fillon','hamon','melenchon|mélenchon','le pen|lepen|mlp']
    resultList = []
    for cand in candidats :
        candidat = candidats.pop(0)
        reg = '|'.join(candidats)
        print(reg)
        pipe = [{"$match":{"$and":[{"t_text":re.compile(cand)},{'t_text':{'$not':re.compile(reg)}},{"t_time":{"$gte":now - 8.64e7}}]}}]
        result = list(collection.aggregate(pipeline=pipe))
        for res in result : res['candidat'] = cand 
        resultList.append(result)
        candidats.append(candidat)
    resultDF = pd.DataFrame(resultList)
    client.close()
    return resultDF


def buildMatrix(tweetsDf):
    

    return tweetsDf




def predictOpinion(port=27018):
    f = open('/home/raphael/Bureau/sentiment_model.pkl','rb')
    model = pickle.load(f)
    tweetsDf = buildMatrix(extractTweets())
    print(tweetsDf.head(5))
    tweetsDf['sentiment'] = model.predict(X_test)
    client = pym.MongoClient(port=port)
    collection = client.tweet.predicted
    collection.insert_many(tweetsDf.to_dict('records'))
    export = []
    for candidat in tweetsDf['candidat'].unique() :
    	currCand = {}
    	currCand['candidat'] = candidat
    	currCand['négatif'] = np.sum(tweetsDf[tweetsDf['candidat'] == candidat and tweetsDf['sentiment'] == -1]) / tweetsDf[tweetsDf['candidat'== candidat]].shape[0]
    	currCand['neutre'] = np.sum(tweetsDf[tweetsDf['candidat'] == candidat and tweetsDf['sentiment'] == 0]) / tweetsDf[tweetsDf['candidat'== candidat]].shape[0]
        currCand['positif'] = np.sum(tweetsDf[tweetsDf['candidat'] == candidat and tweetsDf['sentiment'] == 1]) / tweetsDf[tweetsDf['candidat'== candidat]].shape[0]
        export.append(currCand)
    file = open('opinions.json','w')
    json.dumps(file, export)



predictOpinion()