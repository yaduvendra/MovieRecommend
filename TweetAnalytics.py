import DataService
import pymongo
import time
import re
import math
from textblob import TextBlob

# Sentiment degree calculation is referring Visualizing Twitter Sentiment from NCSU
# https://www.csc.ncsu.edu/faculty/healey/tweet_viz/

# Text Processing reference: https://textblob.readthedocs.org/en/dev/index.html

class Sentiment(object):

    @classmethod
    def __init__(self):
        mongo = DataService.Mongo("anew")
        anewDoc = mongo.db["list"].find_one({"type": "all"})
        self.anewDict = anewDoc["dict"]
        print("[Sentiment] ANEW list retrieved.")

    @classmethod
    def gain_sentiment(self, sentence):
        words = tokenize(sentence)
        if len(words) < 2:
            return 0
        valence_list = []
        for word in words:
            if word in self.anewDict:
                valence_list.append([self.anewDict[word]["valence_mean"], self.anewDict[word]["valence_sd"]])

        if len(valence_list) < 2:
            return 0

        weight_sum = 0
        value_sum = 0
        for cur in valence_list:
            cur_weight = self.probability_density(cur[1])
            weight_sum += cur_weight
            value_sum += cur[0] * cur_weight
        return value_sum / weight_sum

    @classmethod
    # https://en.wikipedia.org/wiki/Probability_density_function
    def probability_density(self, sd):
        return 1 / (sd * math.sqrt(2 * math.pi))

# unfinished
def tokenize(sentence):
    # words = re.split("\s|\.|;|,|\*|\n|!|'|\"", sentence)
    text = TextBlob(sentence)
    words = text.words
    res = []
    for word in words:
        if len(word) > 0:
            res.append(stemming(word))
    # print(res)
    return res

# unfinished
# handle empty or invalid word, and stem word
def stemming(word):
    return word.lower()


def main():
    sentiment = Sentiment()
    # sentence = "Congrats to @HCP_Nevada on their health care headliner win"
    # sentence = "b'I love you @iHeartRadio! I love you hooligans! love you Sriracha. I love you @LeoDiCaprio. Thinking of u @holyfield  https://t.co/iPoHf03G4R'"
    sentence = "The secret life of Walter Mitty is a fantastic movie"
    print("[TweetAnalytics] Evaluating sentence: " + sentence)
    score = sentiment.gain_sentiment(sentence)
    print("[TweetAnalytics] Sentiment score: " + str(score))

if __name__ == "__main__":
    main()