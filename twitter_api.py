from __future__ import unicode_literals
import tweepy
import pickle
import time
import os

consumer_key =  os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_secret = os.environ['TWITTER_access_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def get_tweets(topic, save_file_name, num_batches=25): # num_batches * 100 is total tweets target
    tweets = set()
    # public_tweets = api.home_timeline()
    for i in xrange(num_batches):
        try:
            print 'Loading', i+1, 'of', num_batches
            for tweet in tweepy.Cursor(api.search, q=topic).items(100): #100 batches of 20

                if tweet.lang == 'en':
                    tweets.add(tweet.text) #the text .text
                    #tweet.add(tweet.text._json['user']['location'])

            time.sleep(35) #brent uses 35
        except:
            print 'Waiting for API to allow more calls...'
            time.sleep(60) #brent uses 60
            pass
    pickle.dump( tweets, open( "{}.pkl".format(save_file_name), "wb" ) )
    print 'Succesfully pickled', len(tweets), 'tweets!'



if __name__ == '__main__':
    get_tweets('are', 'tweets/tweets_02_08_are', 100) #batch size 25
