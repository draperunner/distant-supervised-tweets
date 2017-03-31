import re

# Files
POSITIVE_FILE = 'tweets.pos.tsv'
NEGATIVE_FILE = 'tweets.neg.tsv'
NEUTRAL_FILE = 'tweets.neu.tsv'

# MongoDB connection
DB_NAME = "tweets"
COLLECTION_NAME = "semeval"
QUERY = ""

SAVE = False

VERBOSE = False

def default_preprocess(tweet):
    return re.sub(r"\s+", " ", tweet)  # Normalize whitespace. Replace tabs and newlines with single spaces


PREPROCESS = default_preprocess
