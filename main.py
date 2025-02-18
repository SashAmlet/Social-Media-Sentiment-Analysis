from data import GetData
from datetime import datetime
from SentimentAnalyzer import RedditSentimentAnalyzer


# List of subreddits for different countries
subreddits = {
    "USA": "usa",
    "Russia": "AskARussian",
    "Ukraine": "ukraine",
    "UK": "unitedkingdom",
    "Germany": "germany",
    "France": "france",
    "China": "china"
}

# Fetch tweets and save them to a file
# posts = GetData.fetch_reddit_posts(subreddits, 100, 5)

# GetData.save_reddit_posts(posts, 'reddit_posts2.json')


analyzer = RedditSentimentAnalyzer('reddit_posts2.json', subreddits)
analyzer.run_analysis(load_from_file=True, filename='sentiments_20250218_153956.json')