import tweepy
import json
import random
from dotenv import load_dotenv
import os
import praw
import time
import pandas as pd
from datetime import datetime, timedelta
import requests

class GetData:

    @staticmethod
    def fetch_tweets(start_date, end_date, num_of_tweets):
        # Loading environment variables from .env file
        load_dotenv()

        bearer_token = os.getenv('BEARER_TOKEN')

        # Authenticate to Twitter using Bearer Token for API v2
        client = tweepy.Client(bearer_token=bearer_token)

        tweets = []
        query = "#UKRAINE lang:en"
        
        # Convert dates to ISO format
        start_time = start_date.isoformat() + "Z"
        end_time = end_date.isoformat() + "Z"

        response = client.search_recent_tweets(query=query, start_time=start_time, end_time=end_time, max_results=num_of_tweets)

        for tweet in response.data:
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

    @staticmethod
    def fetch_reddit_posts(num_ot_posts=10, num_ot_comments=5):
        
        # Loading environment variables from .env file
        load_dotenv()

        REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
        REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
        REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        # Список сабреддитів для різних країн
        subreddits = {
            "USA": "usa",
            "Russia": "AskARussian",
            "Ukraine": "ukraine",
            "UK": "unitedkingdom",
            "Germany": "germany",
            "France": "france",
            "China": "china"
        }
        
        posts = {}
    
        for country, subreddit_name in subreddits.items():
            print(f"Fetching posts from {subreddit_name}...")
            country_posts = []
            
            # Пошук постів з ключовим словом "Ukraine" у зазначених сабреддитах
            for post in reddit.subreddit(subreddit_name).search("Ukraine", limit=num_ot_posts):
                # Отримуємо перші n коментарів
                post.comments.replace_more(limit=0)  # Це дозволяє отримати всі коментарі
                comments = [comment.body for comment in post.comments[:num_ot_comments]]  # Беремо перші n коментарів
                
                # Преобразуем объект post в словарь, извлекая только нужные данные
                post_data = {
                    'subreddit': subreddit_name,
                    'title': post.title,
                    'url': post.url,
                    'text': post.selftext,  # текст самого поста
                    'comments': comments   # Додаємо коментарі
                }
                country_posts.append(post_data)
                time.sleep(0.1)
            
            posts[country] = country_posts
            print(f"Found {len(country_posts)} posts for {country}")
        
        return posts
    
    @staticmethod
    def save_reddit_posts(posts, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)