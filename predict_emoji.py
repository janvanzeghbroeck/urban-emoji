import cPickle as pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


class Emoji(object):

    def __init__(self):
        # fit the Naive Bayes
        np.random.seed(42)
        self.emojis = pd.read_pickle('../database/df_emojis.pkl')

    def fit(self):

        # ------- this part needs work
        try:
            self.labeled_tweets = pd.read_pickle('../database/labeled.pkl')
            print 'it worked'
        except:
            from label_tweets import label_tweets
            tweets = np.array(list(pickle.load(open('../database/yay_moji.pkl','rb'))))
            self.by_emoji,self.labeled_tweets = label_tweets(tweets,self.emojis,top = 50, save = True)

        self.y = self.labeled_tweets['emoji'].values
        self.X = self.labeled_tweets['tweet'].values


    def model(self, max_df_ = .8, min_df_ = .001, ngram = (1,2)):

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X,self.y)

        stopwords = set(list(ENGLISH_STOP_WORDS) + ['rt', 'follow', 'dm', 'https', 'ur', 'll' ,'amp', 'subscribe', 'don', 've', 'retweet', 'im', 'http','lt'])

        # fit the tfidf or CountVectorizer
        self.tfidf = TfidfVectorizer(max_features=10000, max_df = max_df_, min_df=min_df_, stop_words = stopwords, ngram_range = ngram)

        self.tfidf.fit(self.X_train)
        self.vector = self.tfidf.transform(self.X_train)

        # --> add the emoji name to bag of words for each emoji
        self.bag = np.array(self.tfidf.get_feature_names())

        self.nb = GaussianNB()
        self.nb.fit(self.vector.todense(), self.y_train)

    def internal_predict(self, print_side_by_side = True):
        test_tfidf = self.tfidf.transform(self.X_test)
        predicted = self.nb.predict(test_tfidf.todense())
        print 'labeled'
        acc = np.mean(self.y_test == predicted)

        print 'Test accuracy =',acc
        print ''

        if print_side_by_side:
            for true,predict in zip(self.y_test,predicted):
                print '-->',true,predict


    def predict(self,text):
        top_n = 3
        test_tfidf = self.tfidf.transform([text])
        probs = self.nb.predict_proba(test_tfidf.todense())
        probs = probs.flatten()
        above_0 = np.argwhere(probs>0).flatten()
        above_0 = np.sort(above_0)[::-1]
        print '-->',text,'=',
        for i in above_0[:5]:
            print self.nb.classes_[i],' ',#probs.flatten()[i],' ',
        print ''

        return probs

    def print_top_words(self,top_n_words=5):
        # printing top words for each emoji
        print ''
        print '----- Top {} words for each Emoji in Train set'.format(top_n_words)
        print '-'*60
        for i in range(len(self.nb.classes_)):
            top =  self.bag[self.nb.theta_[i].argsort()[::-1]][:top_n_words]
            print self.nb.classes_[i],' -->',top
        print ''



if __name__ == '__main__':

    # run clean_tweets
    # run labeled_tweets

    emo = Emoji()
    emo.fit()
    emo.model()
    b = emo.predict('good night, i love you')
    c = emo.predict('i am so worried about my exam tomorrow')
    d = emo.predict('does this model do a good job')
    e = emo.predict('who am i and what is happening')
    e = emo.predict('oh baby baby baby oh')
    e = emo.predict('my iphone screen is cracked')
    e = emo.predict('2017 is so far the best year')
    e = emo.predict('to be or not to be that is the question')
    e = emo.predict('my bf is the best')
    a = emo.predict('i want a divorce')
    e = emo.predict('tell me about your life')
    e = emo.predict('that was the last thing i needed')
    e = emo.predict('i pitty the fool')
    e = emo.predict('i need coffee')
    e = emo.predict('la la land')
    e = emo.predict('netflix and chill')
    e = emo.predict('i am thankful to be alive')
    e = emo.predict('curse word')
    e = emo.predict('donald trump')
    e = emo.predict('sexy weekend')
    e = emo.predict('who has two thumbs and a great additude this guy')

    # emo.internal_predict(print_side_by_side = True)
    # emo.print_top_words(5)
