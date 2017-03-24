from afinn import Afinn
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import methods.defaults as d
from methods.method import Method


class ComboTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db=d.DB, collection=d.COLLECTION, query=d.COLLECTION, preprocess=d.PREPROCESS,
                 subjectivity_threshold=0.1, polarity_threshold=0, save=d.SAVE, verbose=d.VERBOSE, a=1, b=1, c=1, d=3):
        Method.__init__(self, name="TEXTBLOB", db=db, collection=collection, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save, verbose=verbose)
        self.subjectivity_threshold = subjectivity_threshold
        self.polarity_threshold = polarity_threshold
        self.afinn = Afinn(emoticons=True)
        self.vader = SentimentIntensityAnalyzer()

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def classify(self, tweet):

        if self.a + self.b + self.c == 0:
            return "neutral"

        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity

        afinn_score = self.afinn.score(tweet)
        vader_score = self.vader.polarity_scores(tweet)

        # Normalize scores to be between -1 and +1
        norm_afinn = afinn_score / (5 * len(tweet.split()))
        norm_vader = vader_score["compound"]
        norm_blob = polarity

        score = (self.a * norm_afinn + self.b * norm_vader + self.c * norm_blob) / (self.a + self.b + self.c)

        if score > self.d / 10.:
            return "positive"
        if score < -self.d / 10.:
            return "negative"

        return "neutral"
