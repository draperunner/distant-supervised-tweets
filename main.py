import re

import multiprocessing
import preprocessor as p
from pymongo import MongoClient

from methods.afinn_tweets import AfinnTweets
from methods.vader_tweets import VaderTweets
from methods.combo_tweets import ComboTweets
from methods.lexicon_classifier import LexiconClassifier
from methods.textblob_tweets import TextblobTweets
from methods.emoticon_tweets import EmoticonTweets
from methods.emoticon_extended_tweets import EmoticonExtendedTweets
from time import time

# MongoDB query
query = {
    # English tweets only
    'lang': 'en',
    # No retweets
    'retweeted_status': {
        '$exists': False
    },
    # No tweets with ◦ symbol, as they are usually weather reports.
    # No tweets that end with a number. Often spam.
    'text': {
        '$not': re.compile("^.*°.*$|^.*\d$"),
    },
    # No tweets with urls
    '$or': [
        {
            "entities.urls": {
                "$exists": False
            }
        },
        {
            "entities.urls": {
                "$size": 0
            }
        }
    ],
}


# Preprocessing methods
def clean_url_mention(tweet):
    norm_text = re.sub(r"\s+", " ", tweet)  # Normalize whitespace. Replace tabs and newlines with single spaces
    p.set_options(p.OPT.URL, p.OPT.MENTION)
    text = p.clean(norm_text)  # Remove user mentions and urls
    return text


def clean_all(tweet):
    norm_text = re.sub(r"\s+", " ", tweet)  # Normalize whitespace. Replace tabs and newlines with single spaces
    p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.NUMBER)
    return p.clean(norm_text)  # Remove user mentions and urls


def grid_search_vader(m, n):
    """
    TEXTBLOB, no preprocessing
    """
    for i in range(m, n):
        VaderTweets(query=query, threshold=i / 10.).run().test().latex()


def grid_search_textblob(m, n):
    """
    TEXTBLOB, no preprocessing
    """
    for i in range(m, n):
        for j in range(m, n):
            # print("subjectivity", i / 10., "polarity", j / 10.)
            TextblobTweets(query=query, subjectivity_threshold=i / 10.,
                           polarity_threshold=j / 10.).run().test().latex(i / 10., j / 10.)


def grid_search_combo_tweets(m, n):
    t = time()
    best_performing = []
    for a in range(m, n):
        for b in range(m, n):
            for c in range(m, n):
                for d in range(0, 4):
                    if a == b == c and a > 1:
                        continue
                    ct = ComboTweets(query=query, a=a, b=b, c=c, d=d).run().test()
                    best_performing.append(ct)
        print("a", a, time() - t)

    best_performing.sort(key=lambda q: q.F1_pnn)
    for x in best_performing[-10:]:
        x.latex(x.a / 10., x.b / 10., x.c / 10., x.d / 10.)


def tooopl(a, b):
    tuples = []
    for i in range(a, b):
        for j in range(a, b):
            tuples.append((i, j))
    return tuples

# grid_search_vader(1, 9)
# grid_search_textblob(1, 4)
# grid_search_combo_tweets(0, 5)

def compare_methods():
    AfinnTweets(query=query).run().test().latex()
    EmoticonTweets(query=query).run().test().latex()
    EmoticonExtendedTweets(query=query).run().test().latex()
    VaderTweets(query=query, threshold=0.1).run().test().latex()
    TextblobTweets(query=query, subjectivity_threshold=0.1, polarity_threshold=0.3).run().test().latex()
    LexiconClassifier(query=query).run().test().latex()
    ComboTweets(query=query, a=0, b=4, c=4, d=2).run().test().latex()
    ComboTweets(query=query, a=3, b=1, c=1, d=1).run().test().latex()

compare_methods()
