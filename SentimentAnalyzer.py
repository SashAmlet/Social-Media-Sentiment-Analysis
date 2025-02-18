import json
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from analyze import TextProcessor
from datetime import datetime

class RedditSentimentAnalyzer:
    def __init__(self, filename, subreddits):
        self.filename = filename
        self.data = self.load_data()
        self.analyzer = TextProcessor()
        self.subreddits = subreddits

    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def analyze_sentiments(self, save_to_file=True):
        sentiments = []
        for country, posts in self.data.items():
            for post in posts:
                if post['text'] != '':
                    sentiment, processed_text = self.analyzer.analyze_sentiment(post['text'])
                    if sentiment['compound'] != 0:
                        sentiments.append({
                            'country': country,
                            'title': post['title'],
                            'sentiment': sentiment,
                            'text': post['text'],
                            'processed_text': processed_text
                        })
                for comment in post['comments']:
                    sentiment, processed_text = self.analyzer.analyze_sentiment(comment)
                    if sentiment['compound'] != 0:
                        sentiments.append({
                            'country': country,
                            'title': post['title'],
                            'sentiment': sentiment,
                            'text': comment,
                            'processed_text': processed_text
                        })


        df = pd.DataFrame(sentiments)

        if save_to_file:
            # Generate a unique file name using the current date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'sentiments_{timestamp}.json'

            # Saving a DataFrame to a JSON File with a Unique Name
            df.to_json(filename, orient='records', lines=True)

        return df
    
    
    def plot_sentiment_distribution(self, df):
        # Initializing counters for each mood type
        sentiment_counts = {'neg': 0, 'neu': 0, 'pos': 0}

        # Calculating the maximum values ​​for each mood type
        for sentiment in df['sentiment']:
            max_sentiment = max((k for k in sentiment if k != 'compound'), key=sentiment.get)
            sentiment_counts[max_sentiment] += 1

        plt.bar(sentiment_counts.keys(), sentiment_counts.values())
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.show()

    def plot_sentiment_over_regions(self, df):        
        # Create a new DataFrame to store the average sentiment.compound across countries
        avg_sentiment_by_country = df.groupby('country')['sentiment'].apply(lambda x: x.apply(lambda y: y['compound']).mean()).reset_index()


        avg_sentiment_by_country.set_index('country', inplace=True)
        avg_sentiment_by_country = avg_sentiment_by_country.reindex(self.subreddits.keys())
        avg_sentiment_by_country.plot(kind='bar', legend=False)
        plt.title('Average Sentiment Compound by Country')
        plt.xlabel('Country')
        plt.ylabel('Average Sentiment Compound')
        plt.xticks(rotation=45)
        plt.show()

    def generate_word_cloud(self, df, sentiment, country):
        # Filter data by country
        country_df = df[df['country'] == country]
        
        # Filtering data by sentiment
        if sentiment == 'Positive':
            filtered_df = country_df[country_df['sentiment'].apply(lambda x: max(x, key=x.get) == 'pos')]
        elif sentiment == 'Negative':
            filtered_df = country_df[country_df['sentiment'].apply(lambda x: max(x, key=x.get) == 'neg')]
        else:
            filtered_df = country_df[country_df['sentiment'].apply(lambda x: max(x, key=x.get) == 'neu')]

        # Merging texts
        text = ' '.join(filtered_df['processed_text'])

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {sentiment} Sentiment in {country}')
        plt.show()

    def run_analysis(self, load_from_file=False, filename='sentiments.json'):
        if load_from_file:
            df = pd.read_json(filename, lines=True)
        else:
            df = self.analyze_sentiments()

        
        self.plot_sentiment_distribution(df)
        self.plot_sentiment_over_regions(df)
        
        for country in df['country'].unique():
            self.generate_word_cloud(df, 'Positive', country)
            self.generate_word_cloud(df, 'Negative', country)
            self.generate_word_cloud(df, 'Neutral', country)
            