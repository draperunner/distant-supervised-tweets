import re

import preprocessor as p
from pymongo import MongoClient

from methods.combo_tweets import ComboTweets
from methods.textblob_tweets import TextblobTweets

# MongoDB connection
client = MongoClient()
db = client.test
collection = db.semeval

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


# Print
total_num_tweets = collection.find().count()
print("Total number of tweets:", total_num_tweets)


def grid_search_textblob(m, n):
    """
    TEXTBLOB, no preprocessing
    """
    for i in range(m, n):
        for j in range(m, n):
            print("subjectivity", i / 10., "polarity", j / 10.)
            TextblobTweets(db=db, collection=collection, query=query, subjectivity_threshold=i / 10.,
                           polarity_threshold=j / 10.).run().test().print()


def grid_search_combo_tweets(m, n):
    for a in range(m, n):
        for b in range(m, n):
            for c in range(m, n):
                for d in range(m, n):
                    print(a, b, c, d / 10.)
                    if a == b == c and a > 1:
                        continue
                    ComboTweets(db=db, collection=collection, query=query, a=a, b=b, c=c, d=d).run().test().print()


# grid_search_textblob(1, 4)
# grid_search_combo_tweets(0, 10)

TextblobTweets(db=db, collection=collection, query=query, subjectivity_threshold=0.1, polarity_threshold=0.3,
               save=True, verbose=True).run().test().print()
