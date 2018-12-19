import tweepy
import re
from flask import Flask, jsonify, request
from textblob import TextBlob

app = Flask(__name__)

class SentimentAnalyzer(object):

    def __init__(self):
        consumer_key = "Your API key"
        consumer_key_secret = "Your API secret"
        access_token = "Your access token"
        access_token_secret = "your access token secret"
        self.tweet = {}

        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication failed")

    def clean_tweet(self, text):
        return " ".join(re.sub("(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", text).split())

    def get_tweet_sentiment(self, text):
        analysis = TextBlob(self.clean_tweet(text))
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

    def get_tweets(self, query, count=20):
        temp_list = []
        try:
            fetched_data = self.api.search(q=query, count=count)
            for tweet in fetched_data:
                temp_data = {
                    "id"                : tweet.id,
                    "text"              : tweet.text,
                    "name"              : tweet.user.name,
                    "screen_name"       : tweet.user.screen_name,
                    "profile_image_url" : tweet.user.profile_image_url,
                    "sentiment"         : self.get_tweet_sentiment(tweet.text)
                    }
                temp_list.append(temp_data)
            self.tweet = {
                "status" : "OK",
                "tweets" : temp_list
            }
        except tweepy.TweepError as error:
            print("Error: " + str(error))

    def json_object(self):
        return jsonify(self.tweet)

@app.route('/search')
def get():
    data = SentimentAnalyzer()
    query = request.args.get("query")
    data.get_tweets(query)
    return data.json_object()

@app.route('/')
def index():
    return "<h1> This is my twitter sentiment API </h1>"

if __name__ == '__main__':
    app.run(debug=True)