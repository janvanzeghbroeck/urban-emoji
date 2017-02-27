import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
import math
from collections import Counter
import re

def find_emoji(word,df_emoji):
    options = []
    for i, name in enumerate(df_emoji['short_name']):
        if word in name:
            options.append((name,df_emoji['unichar'][i]))
            print name,df_emoji['unichar'][i]
    return options

def get_emojis(tweet_lst,df_emoji):
    emoji_idx = []
    emoji_char =[]
    for tweet in tweet_lst:
        for i,uni in enumerate(df_emoji['unichar']):
            if uni in tweet:
                 emoji_idx.append(i)
                 emoji_char.append(uni)
    return emoji_idx, emoji_char

def get_emojis_by_tweet(tweet_lst,df_emoji):
    by_tweet = []

    for tweet in tweet_lst:
        emoji_char =[]
        for i,uni in enumerate(df_emoji['unichar']):
            if uni in tweet:
                 emoji_char.append(uni)
        by_tweet.append(emoji_char)
    return by_tweet

#this seems to get some emojis that i dont but also missed some that i do. It also get duplicates per tweet that i dont
# def get_emojis_2(tweet_lst):
#     emojis = []
#     for tweet in tweet_lst:
#         emoji = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
#         emojis.append(emoji.findall(tweet))
#     return emojis

def print_emoji(tweet,emoji_char):
    for uni in emoji_char:
        if uni in tweet:
            print uni,


if __name__ == '__main__':
    tweets = np.array(list(pickle.load(open('yay_moji.pkl','rb'))))
    # type is list

    emojis = pd.read_pickle('df_emojis.pkl')
    # type is DataFrame



    # ------------- tfidf
    stopwords = set(list(ENGLISH_STOP_WORDS) + ['rt', 'follow', 'dm', 'https', 'ur', 'll' ,'amp', 'subscribe', 'don', 've', 'retweet', 'im', 'http'])

    tfidf = TfidfVectorizer(max_features=10000, max_df=0.05, min_df=0.001, stop_words = stopwords)

    #lemmetizing need to consider cleaning the tweets myself

    tfidf_tweets = tfidf.fit_transform(tweets)
    bag = np.array(tfidf.get_feature_names())

    # -------------- NMF
    k = 10
     #number of groups
    nmf2 = NMF(n_components = k)
    nmf2.fit(tfidf_tweets)
    W = nmf2.transform(tfidf_tweets) #len(yay_moji,k)
    H = nmf2.components_ #k,len(yay_moji)


    # --------------- Printing Top 10
    tweet_lst = []
    top = 10
    for group in range(k):
        #idx of the top ten words for each group
        i_words = np.argsort(H[group])[::-1][:top]
        words = bag[i_words]

        # idx of the top ten tweets for each group
        i_emojis = np.argsort(W[:,group])[::-1][:top]
        # most common 10 emojis for each group

        print '-'*10
        print 'Group:',group
        for word in words:
            print '#',word
        for i_tweet in i_emojis:
            print_emoji(tweets[i_tweet], emojis['unichar'])
            tweet_lst.append(tweets[i_tweet])
        ind, emo_lst = get_emojis(tweets[i_emojis],emojis)
        # find percentage of emoji per group
        most_emoji, how_many = Counter(emo_lst).most_common(1)[0]
        score = float(how_many)/top
        print score #score is not perfect - similar emojis and repeat in the same tweet
        print '\n'

    # --------------- printing most common emojis
    most_common = 50
    b,all_emojis = get_emojis(tweets,emojis)
    count = Counter(all_emojis).most_common(most_common)
    unicode_top = []
    for emo, i in count:
        print emo,i
        for j, char in enumerate(emojis['unichar']):
            if char == emo:
                unicode_top.append(emojis['unified'][j])


# test stuff
    jan = get_emojis_by_tweet(tweets[0:100],emojis)
    for tweet in jan:
        for emo in tweet:
            print emo,
        print ''
    # name_of = find_emoji('heart',emojis)


    '''
    to do's
    --> how big are the groups? do a most common
    --> get a better score system
    --> allow for tweets with multiple emojis
    --> sub set for tweets with a specific emoji
    --> commonly combined emojis
    --> naive bayes
        prediction accuracy between emojis for how similar they are

    whats the purpose:
    --> to help use emojis as labels for tweets
    '''
