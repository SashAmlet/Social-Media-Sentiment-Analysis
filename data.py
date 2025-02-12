import tweepy
import json
import random
from dotenv import load_dotenv
import os

class TwitterData:
    @staticmethod
    def fetch_tweets(num_of_tweets, num_of_words):

        # Loading environment variables from .env file
        load_dotenv()

        api_key = os.getenv('API_KEY')
        api_secret_key = os.getenv('API_SECRET_KEY')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        # Authenticate to Twitter
        auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Generate random hashtags
        hashtags = ['#Putin', '#Zelensky', '#STAYWITHUKRAINE', '#WAR', '#RUSSIA', '#UKRAINE']
        random_hashtags = random.sample(hashtags, num_of_tweets)

        tweets = []
        for hashtag in random_hashtags:
            for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, lang="en").items(num_of_tweets):
                if len(tweet.text.split()) <= num_of_words:
                    tweets.append(tweet._json)

        return tweets

    @staticmethod
    def save_tweets(tweets, filename):
        with open(filename, 'w') as file:
            json.dump(tweets, file, indent=4)

# Example usage:
# tweets = TwitterData.fetch_tweets(api_key, api_secret_key, access_token, access_token_secret, 10, 10)
# TwitterData.save_tweets(tweets, 'tweets.json')