from __future__ import unicode_literals
import tweepy
import pickle
import os
import datetime
import time
import re
import boto
# import time



'''

$ pip install tweepy
move .pem file with atom to .ssh
cd .ssh
$ chmod 400 tweets.pem
change config file
$ ssh tweets

moving files to the ubuntu
$ scp -i tweets.pem ~/path/folder/file tweets: ~/


upload twitter keys

$ ls -a
# .zshrc == .bash_profile
$ nano .zshrc
    scroll down with buttons copy and paste then follow insructions to not fuck it up (^ == control)
    $ ^X
    $ Y
    $ 'enter'

$ source .zshrc
to est
$ echo $TWITTER_access_token



delete a file
$ rm filename

delete all files from a folder
$ rm folder/*

'''

# twitter stuff
consumer_key =  os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_secret = os.environ['TWITTER_access_secret']

# aws stuff
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)




def get_tweets(topic, save_file_name, num_batches=25, num_tweets = 20, to_bucket = False): # num_batches * 100 is total tweets target
    tweets = set()
    # public_tweets = api.home_timeline()
    for i in xrange(num_batches):
        try:
            print 'Loading', i+1, 'of', num_batches
            for tweet in tweepy.Cursor(api.search, q=topic).items(num_tweets): #100 batches of 20

                if tweet.lang == 'en':
                    tweets.add(tweet.text) #the text .text
                    #tweet.add(tweet.text._json['user']['location'])

            time.sleep(35) #brent uses 35
        except:
            print 'Waiting for API to allow more calls...'
            time.sleep(60) #brent uses 60
            pass

    # if to_bucket:
        pass
    else:
        pickle.dump( tweets, open( "../tweets/{}.pkl".format(save_file_name), "wb" ) )
        print 'Succesfully pickled', len(tweets), 'tweets!'



if __name__ == '__main__':
    now = datetime.datetime.today().ctime()
    now = re.sub(' ','_',now)
    now = re.sub(':','-',now)
    # date = time.strftime("%m-%d-%Y-%H-%M") # month, day, year, hour, min


    # use boto to connect to aws buckets
    conn = boto.connect_s3(aws_access_key, aws_access_secret_key)

    # what bucket?
    bucket_name = 'urban-emoji-tweets'

    # check if bucket exists if not make it
    # if conn.lookup(bucket_name) is None:
    #     b = conn.create_bucket(bucket_name, policy= public-read )
    # else:
    b = conn.get_bucket(bucket_name)

    simple_words = ['is', 'it', 'the', 'are', 'if', 'this','that']

    for word in simple_words:
        pkl_name = '../tweets/tweets_{}_{}'.format(now,word)
        s3_name = 'tweets/tweets_{}_{}.pkl'.format(now,word)
        loc_name = '../tweets/tweets_{}_{}.pkl'.format(now,word)
        get_tweets(word, pkl_name, num_batches = 10, num_tweets = 10)

        # save the pkl file
        file_object = b.new_key(s3_name)#where to save
        file_object.set_contents_from_filename(loc_name)

        # remove the local saved pkl file
        os.remove(loc_name)

        print 'Successfully saved {} to S3 bucket {}'.format(s3_name,bucket_name)

    # to read the file
    # fil_object.get_contents_to_file('folder/file')
