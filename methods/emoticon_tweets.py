import methods.defaults as d
from methods.method import Method


class EmoticonTweets(Method):
    def __init__(self, positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE, neutral_file=d.NEUTRAL_FILE,
                 db_name=d.DB_NAME, collection_name=d.COLLECTION_NAME, query=d.COLLECTION_NAME, preprocess=d.PREPROCESS,
                 save=d.SAVE, verbose=d.VERBOSE):
        Method.__init__(self, name="EMOTICON", db_name=db_name, collection_name=collection_name, query=query, negative_file=negative_file,
                        positive_file=positive_file, neutral_file=neutral_file, preprocess=preprocess, save=save, verbose=verbose)
        self.emoticons = {
            "positive": [":)", ":-)", ": )", ":D", "=D"],
            "negative": [":(", ":-(", ": ("]
        }

    def contains_emoticon(self, sentiment, tweet):
        """
        Checks if a tweet contains an emoticon of given sentiment
        :param sentiment: String, either "positive", "negative" or "neutral"
        :param tweet: A tweet text string
        :return: boolean
        """
        for emoticon in self.emoticons[sentiment]:
            if emoticon in tweet:
                return True

        return False

    def classify(self, tweet):

        # Calculate sentiment scores
        contains_positive = self.contains_emoticon("positive", tweet)
        contains_negative = self.contains_emoticon("negative", tweet)

        if contains_positive and contains_negative:
            return None
        if contains_positive:
            return "positive"
        if contains_negative:
            return "negative"

        return "neutral"
