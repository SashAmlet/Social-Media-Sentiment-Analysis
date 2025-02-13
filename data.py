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
        random_hashtag = random.choices(hashtags, k=1)[0]

        tweets = []
        query = f"{'#UKRAINE'} lang:en"
        response = client.search_recent_tweets(query=query, max_results=num_of_tweets)

        for tweet in response.data:
            if len(tweet.text.split()) >= 0:#num_of_words:
                tweets.append(tweet.data)

        return tweets

    @staticmethod
    def save_tweets(tweets, filename):
        # Checking if the file exists
        if os.path.exists(filename):
            # Loading existing data
            with open(filename, 'r') as file:
                existing_tweets = json.load(file)
        else:
            existing_tweets = []

        # Adding new tweets to existing ones
        existing_tweets.extend(tweets)

        # Save the updated data back to the file
        with open(filename, 'w') as file:
            json.dump(existing_tweets, file, indent=4)