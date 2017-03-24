from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import methods.defaults as d
from methods.method import Method


class VaderTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db=d.DB, collection=d.COLLECTION, query=d.COLLECTION, preprocess=d.PREPROCESS, threshold=0.5,
                 save=d.SAVE, verbose=d.VERBOSE):
        Method.__init__(self, name="VADER", db=db, collection=collection, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save, verbose=verbose)
        self.vader = SentimentIntensityAnalyzer()
        self.threshold = threshold

    def classify(self, tweet):

        vader_score = self.vader.polarity_scores(tweet)

        if vader_score['pos'] >= self.threshold:
            return "positive"
        elif vader_score['neg'] >= self.threshold:
            return "negative"
        elif vader_score['neu'] >= self.threshold:
            return "neutral"
