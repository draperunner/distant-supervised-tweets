from afinn import Afinn

import methods.defaults as d
from methods.method import Method


class AfinnTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db=d.DB, collection=d.COLLECTION, query=d.COLLECTION, preprocess=d.PREPROCESS, save=d.SAVE):
        Method.__init__(self, name="AFINN", db=db, collection=collection, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save)
        self.afinn = Afinn(emoticons=True)

    def classify(self, tweet):

        score = self.afinn.score(tweet)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"
