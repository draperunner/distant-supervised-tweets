from time import time, strftime, gmtime

import methods.defaults as d
from methods.utils import safe_division

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

        # Evaluation metrics
        self.accuracy = None
        self.precision_positive = None
        self.precision_negative = None
        self.precision_neutral = None

        self.recall_positive = None
        self.recall_negative = None
        self.recall_neutral = None

        self.F1_pos = None
        self.F1_neg = None
        self.F1_neu = None
        self.F1_pn = None

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

        num_classified_as = {"positive": 0, "negative": 0, "neutral": 0}
        num_corrects_as = {"positive": 0, "negative": 0, "neutral": 0}
        actuals = {"positive": 0, "negative": 0, "neutral": 0}

        tweets = self.collection.find(self.query)
        for tweet in tweets:
            if tweet['id_str'] not in self.sentiment_map:
                continue
            correct_sentiment = tweet['sentiment']
            prediction = self.sentiment_map[tweet['id_str']]
            actuals[correct_sentiment] += 1
            num_classified_as[prediction] += 1
            if correct_sentiment == prediction:
                if correct_sentiment == "positive":
                    num_corrects_as["positive"] += 1
                elif correct_sentiment == "negative":
                    num_corrects_as["negative"] += 1
                elif correct_sentiment == "neutral":
                    num_corrects_as["neutral"] += 1

        total_num_correct = sum(map(lambda item: item[1], num_corrects_as.items()))
        self.accuracy = safe_division(total_num_correct, num_tweets)

        self.precision_positive = safe_division(num_corrects_as["positive"], num_classified_as["positive"])
        self.precision_negative = safe_division(num_corrects_as["negative"], num_classified_as["negative"])
        self.precision_neutral = safe_division(num_corrects_as["neutral"], num_classified_as["neutral"])

        self.recall_positive = safe_division(num_corrects_as["positive"], actuals["positive"])
        self.recall_negative = safe_division(num_corrects_as["negative"], actuals["negative"])
        self.recall_neutral = safe_division(num_corrects_as["neutral"], actuals["neutral"])

        self.F1_pos = safe_division(2 * self.precision_positive * self.recall_positive, self.precision_positive + self.recall_positive)
        self.F1_neg = safe_division(2 * self.precision_negative * self.recall_negative, self.precision_negative + self.recall_negative)
        self.F1_neu = safe_division(2 * self.precision_neutral * self.recall_neutral, self.precision_neutral + self.recall_neutral)

        self.F1_pn = safe_division(self.F1_pos + self.F1_neg, 2)

        return self

    def print(self):
        """
        Prints a line of execution stats
        :return: self
        """
        print(self.name, self.num_tweets, safe_division(self.num_tweets, self.total_num_tweets), sep="\t\t")
        print("Time\t", str(round(self.run_time, 2)) + ' sec', str(round(1000 * self.run_time / float(self.total_num_tweets), 2)) + ' ms/tweet', sep="\t")
        print("Precision", self.precision_positive, self.precision_negative, self.precision_neutral, sep="\t")
        print("Recall\t", self.recall_positive, self.recall_negative, self.recall_neutral, sep="\t")
        print("F1\t\t", self.F1_pos, self.F1_neg, self.F1_neu, sep="\t")
        print("F1-pn\t", self.F1_pn, sep="\t")
        print("Accuracy", self.accuracy, sep="\t")
        print()

        return self
