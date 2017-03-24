from time import time, strftime, gmtime

import methods.defaults as d


class Method:
    def __init__(self, name="Method", positive_file=d.POSITIVE_FILE, negative_file=d.NEGATIVE_FILE,
                 neutral_file=d.NEUTRAL_FILE,
                 db=d.DB, collection=d.COLLECTION, query=d.QUERY, preprocess=d.PREPROCESS, save=d.SAVE, verbose=d.VERBOSE):

        self.name = name
        self.verbose = verbose

        self.save = save
        self.positive_file = positive_file
        self.negative_file = negative_file
        self.neutral_file = neutral_file

        self.db = db
        self.collection = collection
        self.query = query

        self.sentiment_map = {}

        self.preprocessor = preprocess

        self.total_num_tweets = collection.find().count()
        self.num_tweets = -1
        self.run_time = -1
        self.score = None

    def classify(self, tweet):
        """
        Must be implemented by subclass
        :param tweet: Preprocessed tweet to classify
        :return: A string that is either "positive", "negative" or "neutral"
        """
        return None

    def run(self):
        start_time = time()

        if self.save:
            pos_file = open(self.positive_file, "w+")
            neg_file = open(self.negative_file, "w+")
            neu_file = open(self.neutral_file, "w+")

        tweets = self.collection.find(self.query)
        total_num_tweets = tweets.count()

        for index, tweet in enumerate(tweets):

            # Print progress if verbose
            if self.verbose and index % 10000 == 0:
                print(index, "tweets\t", round(100 * index / float(total_num_tweets)), '%\t', strftime("%H:%M:%S", gmtime(time() - start_time)))

            # Preprocessing
            original_tweet = tweet["text"]
            preprocessed_tweet = self.preprocessor(original_tweet[:])

            predicted_label = self.classify(preprocessed_tweet)

            id_str = tweet["id_str"]

            if predicted_label == "neutral":
                self.sentiment_map[id_str] = 'neutral'
                if self.save:
                    neu_file.write(id_str + "\t" + preprocessed_tweet + "\n")
            elif predicted_label == "positive":
                self.sentiment_map[id_str] = 'positive'
                if self.save:
                    pos_file.write(id_str + "\t" + preprocessed_tweet + "\n")
            elif predicted_label == "negative":
                self.sentiment_map[id_str] = 'negative'
                if self.save:
                    neg_file.write(id_str + "\t" + preprocessed_tweet + "\n")

        self.num_tweets = len(self.sentiment_map)
        self.run_time = time() - start_time

        if self.save:
            pos_file.close()
            neg_file.close()
            neu_file.close()

        return self

    def test(self):
        """
        Calculates the number of correctly classified tweets (accuracy)
        :return: Accuracy
        """
        num_tweets = len(self.sentiment_map)
        num_corrects = 0
        tweets = self.collection.find(self.query)
        for tweet in tweets:
            if tweet['id_str'] not in self.sentiment_map:
                continue
            if tweet['sentiment'] == self.sentiment_map[tweet['id_str']]:
                num_corrects += 1

        self.score = num_corrects / float(num_tweets)

        return self

    def print(self):
        """
        Prints a line of execution stats
        :return: self
        """
        print(self.name, "\t", self.num_tweets, "\t", round(self.run_time, 2), 'sec\t',
              round(1000 * self.run_time / float(self.total_num_tweets), 2), 'ms/tweet\t',
              round(100 * self.score, 2), '%')
        return self
