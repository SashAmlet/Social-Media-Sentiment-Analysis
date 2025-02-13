import re
import string
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TextProcessor:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text: str) -> str:
        # Remove URLs, mentions, hashtags, and special characters
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+|\#', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text

    def normalize_text(self, text: str) -> str:
        # Convert text to lower case
        text = text.lower()
        # Remove stop words and perform lemmatization
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)

    def tokenize_text(self, text: str) -> List[str]:
        # Tokenize text
        tokens = text.split()
        return tokens

    def analyze_sentiment(self, text: str) -> str:
        # Clean, normalize, and tokenize text
        cleaned_text = self.clean_text(text)
        normalized_text = self.normalize_text(cleaned_text)
        tokens = self.tokenize_text(normalized_text)
        processed_text = ' '.join(tokens)

        # Analyze sentiment
        sentiment = self.analyzer.polarity_scores(processed_text)
        compound_score = sentiment['compound']
        
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'