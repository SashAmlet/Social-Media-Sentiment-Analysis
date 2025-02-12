from data import TwitterData

tweets = TwitterData.fetch_tweets(100, 20)
TwitterData.save_tweets(tweets, 'tweets.json')