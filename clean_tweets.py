import pickle
import pandas as pd
import os

# ----- combines all the tweets into one list
def pickle_pile():
    tweets = []
    for pkl_file in os.listdir('tweets'):
        tweets += list(pickle.load(open('tweets/{}'.format(pkl_file),'rb')))
    return list(set(tweets))

# ----- creates the emoji df and adds the unichar
def df_emojis():
    # create full df_emoji
    df = pd.read_pickle('emoji.pkl')

    # create unicode characters for emojis
    unichar = []
    for uni in df['unified'][0:]:
        try:
            s = "\\U%08x" % int(uni, base=16)
            unichar.append(s.decode('unicode-escape'))
        except:
            unichar.append('NaN')

    df['unichar'] = unichar
    return df


# ------------ finding the tweets with emojis
def yay_no(tweets,df_emojis):
    no_moji = []
    yay_moji = []
    for tweet in tweets:
        tweet = unicode(tweet) #some have type tweepy.models.Status
        yay = False
        for uni in df_emojis['unichar']:
            #if emoji in str(tweet):
            if uni in tweet:
                yay = True
        if yay:
            yay_moji.append(tweet)
        else: # else statement to create no_moji list
            no_moji.append(tweet)
    return yay_moji, no_moji


if __name__ == '__main__':

    tweets = pickle_pile()

    df_emojis = df_emojis()
    df_emojis = df_emojis.iloc[0:1013,:] #dont emojis after 1013 yet

    yay_moji, no_moji = yay_no(tweets,df_emojis)

    pickle.dump( yay_moji, open( "yay_moji.pkl", "wb"))
    pickle.dump( df_emojis, open( "df_emojis.pkl", "wb"))
