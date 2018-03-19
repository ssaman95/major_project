import os
import pandas as pd
import sklearn
import tweepy
from tweepy import OAuthHandler

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV


def mnb_classifier(df_train):
    text_clf = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', MultinomialNB()
                        )])
    
    text_clf = text_clf.fit(df_train['text'], df_train['target_value'])
    
    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf__alpha': (1e-2, 1e-3),
 }

    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(df_train['text'], df_train['target_value'])

    return gs_clf


'''
def create_df(csv_file):
    df = pd.read_csv(csv_file)
    feature_label_names = ['text', 'target_value']
    df = (df.loc[:,feature_label_names])
    return df
    '''

'''
def predict(clf, df_tset):
    preds = clf.predict(df_test)
    return preds
    '''


def authorize():
    consumer_key = 'h18ae5spqB99OWaMWcFA5juVk'
    consumer_secret = 'U8SBYeMgechK5cgqX8YS6fpSVFAulXjZn4TswLHXZvy9xfTSfy'
    access_token = '835752364984385541-G3zx5fvuyQ5zAkrs7stTO1HGOJdsqOM'
    access_secret = 'wiFCZzGHDeBeSZ4tM6Ogab4RWUMX57KxOHvm8V1hrYm5E'
     
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
     
    api = tweepy.API(auth)

    return api


def run_rumour_app(url):
    api = authorize()
    #df = create_df('tweets_out.csv')
    df = pd.read_csv("/home/aman/maj_proj_fe/app/tweets_out.csv")
    feature_label_names = ['text', 'target_value']
    df = (df.loc[:,feature_label_names])

    clf = mnb_classifier(df)
    id = url.split('/')[-1]
    tweet = api.get_status(id)
    tweet_text = [tweet.text]
    prediction = clf.predict(tweet_text)
    
    if prediction[0] == 1:
        return 'Rumour'
    else:
        return 'Non-Rumour'
    

