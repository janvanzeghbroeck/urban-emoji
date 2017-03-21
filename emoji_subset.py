import pickle
import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
import math
from collections import Counter
import re
from model_emoji import get_emojis_by_tweet, print_emoji, get_emojis
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split



def sub_set(tweets,emojis,emo_char):
    sub = []
    by_tweets = get_emojis_by_tweet(tweets,emojis)
    for tweet,emos in zip(tweets,by_tweets):
        if emo_char in tweet:
            sub.append((tweet,emos))
    return sub

def wordize(tweet):
    stops = string.digits + '_@'
    words = tweet.split()
    new_words = []
    for word in words:
        yes = True
        for char in stops:
            if char in word:
                yes = False
        if yes:
            new_words.append(word)

    return ' '.join(new_words)


def NB_acc(emo1, emo2, tweets, emoji):
    a = sub_set(tweets,emojis, emo1)
    b = sub_set(tweets,emojis, emo2)
    labels = np.hstack((np.zeros(len(a)),np.ones(len(b))))
    # me and

    tweets_a, emos_a = zip(*a)
    tweets_b, emos_b = zip(*b)

    tweets = list(tweets_a) + list(tweets_b)

# ------------- tfidf
    stopwords = set(list(ENGLISH_STOP_WORDS) + ['rt', 'follow', 'dm', 'https', 'ur', 'll' ,'amp', 'subscribe', 'don', 've', 'retweet', 'im', 'http'])

    tfidf = TfidfVectorizer(max_features=10000, max_df=0.3, min_df = .001, stop_words = stopwords, ngram_range = (1, 2))

    #lemmetizing need to consider cleaning the tweets myself

    tfidf_tweets = tfidf.fit_transform(tweets)
    bag = np.array(tfidf.get_feature_names())


# ------------------ predict this emoji or another

    # ----- train test split
    np.random.seed(2)

    X_train, X_test, y_train, y_test = train_test_split(tfidf_tweets.todense(),labels)

    nb = GaussianNB()
    mod = nb.fit(X_train,y_train)
    y_pred = mod.predict(X_test)

    acc = np.mean(y_test == y_pred)
    return acc


if __name__ == '__main__':
    tweets1 = np.array(list(pickle.load(open('../database/yay_moji.pkl','rb'))))
    # type is list
    emojis = pd.read_pickle('../database/df_emojis.pkl')
    # type is DataFrame

    #removing words with digits and ['_@']
    tweets = [wordize(tweet) for tweet in tweets1]

    sparkle = u'\u2728'
    laugh_cry = u'\U0001f602'
    heart_face = u'\U0001f60d'
    praise = u'\U0001f64c'
    earth = u'\U0001f30d'

    a,b=get_emojis(tweets, emojis)

    n = 100 #must be even

    # do a similarity matrix instead
    emoji_choice = Counter(b).most_common(100)
    rnd = np.random.randint(0,100,n)
    half_rnd = zip(rnd[:n/2],rnd[n/2:])
    connections = []
    b = emoji_choice
    # for a, b in half_rnd:
    for b in range(10):
        a = 0
        emo1 = emoji_choice[a][0]
        num1 = emoji_choice[a][1]
        emo2 = emoji_choice[b][0]
        num2 = emoji_choice[b][1]
        acc = NB_acc(emo1, emo2, tweets, emojis)
        connections.append([emo1, num1, emo2, num2, acc])
        print emo1, num1, emo2, num2, acc
    emo1, num1, emo2, num2, acc = zip(*connections)

    sorted_best = np.argsort(acc)[::-1]
    for i in sorted_best:
        print emo1[i],num1[i],emo2[i],num2[i],acc[i]
