import json
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from analyze import TextProcessor
from datetime import datetime

class RedditSentimentAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.analyzer = TextProcessor()

    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def analyze_sentiments(self, save_to_file=True):
        sentiments = []
        for country, posts in self.data.items():
            for post in posts:
                if post['text'] != '':
                    sentiment = self.analyzer.analyze_sentiment(post['text'])
                    sentiments.append({
                        'country': country,
                        'title': post['title'],
                        'sentiment': sentiment,
                        'text': post['text']
                    })
                for comment in post['comments']:
                    sentiment = self.analyzer.analyze_sentiment(comment)
                    sentiments.append({
                        'country': country,
                        'title': post['title'],
                        'sentiment': sentiment,
                        'text': comment
                    })


        df = pd.DataFrame(sentiments)

        if save_to_file:
            # Generate a unique file name using the current date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'sentiments_{timestamp}.json'

            # Saving a DataFrame to a JSON File with a Unique Name
            df.to_json(filename, orient='records', lines=True)

        return df

    def run_analysis(self, load_from_file=False, filename='sentiments.json'):
        if load_from_file:
            df = pd.read_json(filename, lines=True)
        else:
            df = self.analyze_sentiments()
            