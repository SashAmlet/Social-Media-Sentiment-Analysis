from data import GetData
from datetime import datetime

# Fetch tweets and save them to a file
posts = GetData.fetch_reddit_posts(1000, num_ot_comments=5)

# tweets = GetData.fetch_tweets(start_date, end_date, 100)
GetData.save_reddit_posts(posts, 'reddit_posts.json')