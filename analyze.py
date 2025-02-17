import re
import string
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from googletrans import Translator
import sys
sys.stdout.reconfigure(encoding='utf-8')


class TextProcessor:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.language = 'english'
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.translator = Translator()

    def translate_to_english(self, text: str) -> str:
        try:
            translated = self.translator.translate(text, dest='en')
            return translated.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

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
        # Translate text to English
        translated_text = self.translate_to_english(text)

        # Clean, normalize, and tokenize text
        cleaned_text = self.clean_text(translated_text)
        normalized_text = self.normalize_text(cleaned_text)

        # Analyze sentiment
        sentiment = self.analyzer.polarity_scores(normalized_text)
        
        return sentiment