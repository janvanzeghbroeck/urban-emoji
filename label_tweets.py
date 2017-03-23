import cPickle as pickle
import numpy as np
import pandas as pd
import os

#-----
def get_emojis(tweets,emojis):
    emoji_idx = []
    emoji_char =[]
    for i, tweet in enumerate(tweets):
        for uni in emojis['unichar']:
            if uni in tweet:
                 emoji_idx.append(i)
                 emoji_char.append(uni)
    return np.array(emoji_idx), np.array(emoji_char)
#-----


def label_tweets(tweets, emojis, top = 50, save = True):
    # only train on the top x emojis

    tweet_idx, chars = get_emojis(tweets,emojis)

    unique_chars = list(set(chars))# unique emojis in unicode char of the tweets i have in tweets

    # create empty dataframe where the index in unique_chars
    byemo = pd.DataFrame()
    byemo['uni'] = unique_chars

    tweet_idxs = []  # list of tweet index for each emoji
    tweet_counts = []   # int number of tweets with that emoji
    tweet_doc = []
    for uni_char in byemo['uni']:
        i_tweet_lst = np.argwhere(chars == uni_char).flatten()
        tweet_lst = tweet_idx[i_tweet_lst]
        tweet_idxs.append(tweet_lst)
        tweet_counts.append(len(tweet_lst))
        tweet_doc.append(' '.join(tweets[tweet_lst]))

    byemo['idxs'] = tweet_idxs
    byemo['counts'] = tweet_counts
    byemo['text'] = tweet_doc

    byemo.sort_values('counts',ascending = False,inplace = True)
    byemo = byemo[:top]

    labeled_tweets_list = []
    for uni,idxs in zip(byemo['uni'], byemo['idxs']):
        for idx in idxs:
            labeled_tweets_list.append([uni, tweets[idx]])

    labeled_tweets = pd.DataFrame(labeled_tweets_list)
    labeled_tweets.columns = ['emoji','tweet']
    labeled_tweets['tweet'].apply(lambda x: unicode(x))
    labeled_tweets['emoji'].apply(lambda x: unicode(x))

    if save:
        labeled_tweets.to_pickle('../database/labeled.pkl')


        # pickle.dump( labeled_tweets_list, open( "../database/labeled.pkl", "wb" ) )
        # labeled_tweets.to_csv("../database/labled.csv")
    return byemo[:top],labeled_tweets

if __name__ == '__main__':
    # with open('../database/yay_moji.pkl', 'r') as f:
    #     tweets = f

    tweets = np.array(list(pickle.load(open('../database/yay_moji.pkl','rb'))))
    emojis = pd.read_pickle('../database/df_emojis.pkl')
    b,l = label_tweets(tweets,emojis,top = 100, save = True)
