from afinn import Afinn

import methods.defaults as d
from methods.method import Method


class AfinnTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db_name=d.DB_NAME, collection_name=d.COLLECTION_NAME, query=d.COLLECTION_NAME, preprocess=d.PREPROCESS, save=d.SAVE, verbose=d.VERBOSE):
        Method.__init__(self, name="AFINN", db_name=db_name, collection_name=collection_name, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save, verbose=verbose)
        self.afinn = Afinn(emoticons=True)

    def classify(self, tweet):

        score = self.afinn.score(tweet)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"
