"""Class to deal with Tweets."""
from tweepy import StreamListener
import json
import time
import sys
import pandas as pd
import pickle
from mechanize import Browser
from urllib2 import urlopen
from time import sleep
import pika
from unidecode import unidecode
import pymongo as pym
import pprint
class SListener(StreamListener):
    """Class SListener to deal with Twitter's status."""

    def __init__(self, api=None, fprefix='streamer'):
        """Init methode to initialize variables."""
        self.api = api
        self.counter = 0
        self.fprefix = fprefix
        self.delout = open('/home/ubuntu/Elections/twitter_elections/delete.txt', 'a')
        # self.sentiment_model = self.load_pkl("sentiment_model")
        self.error = 0

        # setup rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        # set max queue size
        args = {"x-max-length": 120}

        self.channel.queue_declare(queue='twitter', arguments=args)
        #self.text_file = open("/home/ubuntu/Elections/twitter_elections/all_tweets.txt", "a")
        self.br = Browser()

    def on_data(self, data):
        """Deal on data (tweepy method)."""
        if 'in_reply_to_status' in data:
            self.on_status(json.loads(data))

    def on_status(self, status):
        """Deal on tweet (tweepy method)."""
        try:
            client = pym.MongoClient()
            db = client.tweet
            tweets = db.tweet
            if status["lang"] == "fr":
                if status["text"] is not None:
                    #print(status)
                    if status['user'] is not None:
                        tweet_res = {"t_user": status['user'], "t_text": status["text"].encode('utf8').lower(), "t_time": float(status['timestamp_ms']),
                                     "t_id": status['id'],
                                     "t_RToriginal_id": status['retweeted_status']['id'],
                                     "t_RToriginal_fullText": status['retweeted_status']['extended_tweet']['full_text'],
                                     "t_RToriginal_hashtags": status['retweeted_status']['extended_tweet']['entities']['hashtags'],
                                     "t_RToriginal_RTcount": status['retweeted_status']['retweet_count'],
                                     "t_RToriginal_favoriteCount": status['retweeted_status']['favorite_count'],
                                     "t_RToriginal_userPseudo": status['retweeted_status']['user']['screen_name'],
                                     "t_RToriginal_userName": status['retweeted_status']['user']['name'],
                                     "t_RToriginal_userFollowers": status['retweeted_status']['user']['followers_count'],
                                     "t_RToriginal_userFollowing": status['retweeted_status']['user']['friends_count'],
                                     "t_RToriginal_userTweetsCount": status['retweeted_status']['user']['statuses_count'],
                                     "t_RToriginal_userDescription": status['retweeted_status']['user']['description'],
                                     "t_RToriginal_date": status['retweeted_status']['created_at'],
                                     "t_lat": 0.0, "t_lng": 0.0,
                                     "t_state": ""}
                    else:
                        tweet_res = {"t_text": status["text"].encode('utf8'), "t_time": float(status['timestamp_ms']),
                                     "t_RToriginal_id": status['retweeted_status']['id'],
                                     "t_RToriginal_fullText": status['retweeted_status']['extended_tweet']['full_text'],
                                     "t_RToriginal_hashtags": status['retweeted_status']['extended_tweet']['entities']['hashtags'],
                                     "t_RToriginal_RTcount": status['retweeted_status']['retweet_count'],
                                     "t_RToriginal_favoriteCount": status['retweeted_status']['favorite_count'],
                                     "t_RToriginal_userPseudo": status['retweeted_status']['user']['screen_name'],
                                     "t_RToriginal_userName": status['retweeted_status']['user']['name'],
                                     "t_RToriginal_userFollowers": status['retweeted_status']['user']['followers_count'],
                                     "t_RToriginal_userFollowing": status['retweeted_status']['user']['friends_count'],
                                     "t_RToriginal_userTweetsCount": status['retweeted_status']['user']['statuses_count'],
                                     "t_RToriginal_userDescription": status['retweeted_status']['user']['description'],
                                     "t_RToriginal_date": status['retweeted_status']['created_at'],
                                     "t_lat": 0.0, "t_lng": 0.0,
                                     "t_state": ""}
                    self.channel.basic_publish(exchange='', routing_key='twitter', body=json.dumps(tweet_res))
                    print 'tweets slis: ', tweet_res
                    #self.text_file.write(str(tweet_res))
                    tweets.insert_one(tweet_res)
		    print("Tweet inserted into MongoDB")
		    pprint.pprint(tweets.find_one())
                    self.counter += 1
                    print self.counter
        except Exception, e:
            print str(e)
            print 'ERROR'
        return

    def on_delete(self, status_id, user_id):
        """Method to delete tweet based on the @status_id and @user_id."""
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        """Limit tweet based on the @track."""
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        """Error on tweet based on the @status_code."""
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        sleep(10)
        return False

    def on_timeout(self):
        """Timeout method."""
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return

    def load_pkl(self, name):
        """Load obj pickle."""
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
