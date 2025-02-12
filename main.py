from data import TwitterData

tweets = TwitterData.fetch_tweets(10, 20)
TwitterData.save_tweets(tweets, 'tweets.json')