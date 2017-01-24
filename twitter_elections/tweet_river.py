#!/usr/bin/python
"""Get tweet in real time."""
from slistener import SListener
from tweepy import OAuthHandler
import tweepy


# Twitter dev information
access_token = "181993597-vxlcaHIxiBiuWsZmdSnD1BcTdUMxTZLnxgyX0gmR"
access_token_secret = "cgTKEWn79pPgKTbATH5CXrFKe367vNvYte3gYQM0D5iET"
consumer_key = "4O8mxz9VwTyjXKOcjHwmP70yy"
consumer_secret = "wNn61usxR7fgDDGiS0zlb0iTnQ25YxYGykzEMKHxHU4vaSx5Q2"

# Connection to the Twitter API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():
    """Method to get Twitter status in real time."""
    track = ['fillon','jadot','bayrou', 'macron ','mlp','lepen','melenchon', 'poutou', 'dupont-aignan', 'dupontaignan', 'peillon','rugy','hamon', 'pinel','bennhamias','valls','montebourg']

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
