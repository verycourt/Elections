#-*- coding: utf-8 -*-
#!/usr/bin/python
"""Get tweet in real time."""
from slistener import SListener
from tweepy import OAuthHandler
import tweepy


# Twitter dev information
access_token = 
access_token_secret = 
consumer_key =
consumer_secret =

# Connection to the Twitter API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():
    """Method to get Twitter status in real time."""
    track = ['lassalle', 'asselineau', 'fillon','bayrou', 'macron ','mlp','lepen','le pen', 'mélenchon'.decode('utf-8'), 'melenchon','hamon','valls', 'poutou', 'arthaud', 'dupont-aignan', 'dupontaignan', 'juppe']

    listen = SListener(api, 'myprefix')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."
    while True:
        try:
            stream.filter(track=track)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)
            print "error!"
            continue

if __name__ == '__main__':
    main()
