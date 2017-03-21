import pickle
import pandas as pd
import os

# ----- combines all the tweets into one list
def pickle_pile(s3 = False):

    tweets = []
    if s3:
        import boto
        aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
        aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

        # use boto to connect to aws buckets
        conn = boto.connect_s3(aws_access_key, aws_access_secret_key)
        bucket_name = 'urban-emoji-tweets'
        b = conn.get_bucket(bucket_name)

        for i, key in enumerate(b.list(prefix = 'tweets/tweets')):
            filename = key.name
            file_object = b.new_key(filename)
            local_save_path = '../{}'.format(filename)
            file_object.get_contents_to_filename('../{}'.format(filename))
            tweets += list(pickle.load(open(local_save_path,'rb')))
            os.remove(local_save_path)

    for pkl_file in os.listdir('../tweets_og'):
        tweets += list(pickle.load(open('../tweets_og/{}'.format(pkl_file),'rb')))


    return list(set(tweets))

# ----- creates the emoji df and adds the unichar
def df_emojis():
    # create full df_emoji
    df = pd.read_pickle('../database/emoji.pkl')

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


    print 'Running, this may take a while...'
    tweets = pickle_pile(s3 = True)

    df_emojis = df_emojis()
    df_emojis = df_emojis.iloc[0:1013,:] #dont emojis after 1013 yet

    yay_moji, no_moji = yay_no(tweets,df_emojis)

    pickle.dump( yay_moji, open( "../database/yay_moji.pkl", "wb"))
    pickle.dump( df_emojis, open( "../database/df_emojis.pkl", "wb"))

    print 'Succesfully pickled {} tweets and emoji data frame'.format(len(yay_moji))
