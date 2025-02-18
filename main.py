from data import GetData
from datetime import datetime
from SentimentAnalyzer import RedditSentimentAnalyzer

# Fetch tweets and save them to a file
# posts = GetData.fetch_reddit_posts(100, 5)

# GetData.save_reddit_posts(posts, 'reddit_posts2.json')


analyzer = RedditSentimentAnalyzer('reddit_posts.json')
analyzer.run_analysis(load_from_file=True)