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

        bearer_token = os.getenv('BEARER_TOKEN')

        # Authenticate to Twitter using Bearer Token for API v2
        client = tweepy.Client(bearer_token=bearer_token)

        # Generate random hashtags
        hashtags = ['#Putin', '#Zelensky', '#STAYWITHUKRAINE', '#WAR', '#RUSSIA', '#UKRAINE']
        random_hashtag = random.choices(hashtags, k=1)

        tweets = []
        query = f"{random_hashtag} lang:en"
        response = client.search_recent_tweets(query=query, max_results=num_of_tweets)

        for tweet in response.data:
            if len(tweet.text.split()) >= num_of_words:
                tweets.append(tweet.data)

        return tweets

    @staticmethod
    def save_tweets(tweets, filename):
        with open(filename, 'w') as file:
            json.dump(tweets, file, indent=4)

# Example usage:
# tweets = TwitterData.fetch_tweets(api_key, api_secret_key, access_token, access_token_secret, 10, 10)
# TwitterData.save_tweets(tweets, 'tweets.json')