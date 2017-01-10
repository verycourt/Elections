import tweepy
import sys
import pika
import json
import time

access_token = "3170234799-qOw35tM50S5W0MHG9O8VRlZh5j6f7m8GzEuEcQQ"
access_token_secret = "5FBYdB7jwR447aE2XMXeM6yJiSGh0fJMYb9WujBJT5Swm"
consumer_key = "IlPMH3fWCDvzLCn2OS3Qk1D1R"
consumer_secret = "DQKeuoyrl77HBXKkBrNlhJjqyMz3UICBbaoeMTy6QllxjoZi9k"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        #setup rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        #set max queue size
        args = {"x-max-length": 120}
        self.channel.queue_declare(queue='twitter', arguments=args)

    def on_data(self, data):
        '''
        twitter data streaming & store in mongodb
        @args data: tweeter streaming data
        '''
        try:
            tweets = json.loads(data)
            if tweets['coordinates'] == None:
                pass
            else:
                #store relevant tweet attributes
                tweet_text = tweets['text']
                tweet_time = tweets['created_at']
                tweet_lat = tweets['coordinates']['coordinates'][0]
                tweet_lng = tweets['coordinates']['coordinates'][1]
                user_name = tweets['user']['screen_name']
                user_img = tweets['user']['profile_image_url']
                following_count = tweets['user']['friends_count']
                follower_count = tweets['user']['followers_count']
                retweet_count = tweets['retweet_count']
                favourite_count = tweets['favorite_count']
                # #store attributes in a dict
                tweet_res = {"t_text": tweet_text, "t_time": tweet_time, "t_lat": tweet_lat,
                             "t_lng": tweet_lng, "u_name": user_name, "u_img": user_img, "rt_count": retweet_count, "fv_count": favourite_count,
                             "u_following": following_count, "u_follower": follower_count}
                self.channel.basic_publish(exchange='', routing_key='twitter', body=json.dumps(tweet_res))
                print 'tweets stre: ', tweets


        except BaseException, e:
            print(str(e))
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

if __name__ == '__main__':
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
    #filter stream data by location of Amsterdam and language = en
    sapi.filter(locations = [-122.75,36.8,-121.75,37.8])
