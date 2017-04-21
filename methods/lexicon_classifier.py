import fjlc

from methods.method import Method


class LexiconClassifier(Method):
    def __init__(self, **kwargs):
        Method.__init__(self, name="LexiconClassifier", **kwargs)
        self.lexicon_classifier = fjlc.LexiconClassifier()

    def classify(self, tweet):
        return self.lexicon_classifier.classify(tweet).lower()
