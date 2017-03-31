from textblob import TextBlob

import methods.defaults as d
from methods.method import Method


class TextblobTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db_name=d.DB_NAME, collection_name=d.COLLECTION_NAME, query=d.COLLECTION_NAME, preprocess=d.PREPROCESS,
                 subjectivity_threshold=0.1, polarity_threshold=0, save=d.SAVE, verbose=d.VERBOSE):
        Method.__init__(self, name="TEXTBLOB", db_name=db_name, collection_name=collection_name, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save, verbose=verbose)
        self.subjectivity_threshold = subjectivity_threshold
        self.polarity_threshold = polarity_threshold

    def classify(self, tweet):

        # Calculate sentiment scores
        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if subjectivity <= self.subjectivity_threshold and abs(polarity) < self.polarity_threshold:
            return "neutral"
        elif polarity >= self.polarity_threshold:
            return "positive"
        elif polarity <= -self.polarity_threshold:
            return "negative"
