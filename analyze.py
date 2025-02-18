import re
import string
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import spacy
from deep_translator import GoogleTranslator
import sys
sys.stdout.reconfigure(encoding='utf-8')


class TextProcessor:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.language = 'english'
        self.stop_words = set(stopwords.words('english'))
        self.nlp = spacy.load('en_core_web_sm')

    def translate_to_english(self, text: str) -> str:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            if translated is None:
                print(text)
            return translated
        except Exception as e:
            print(f"Translation error: {e}\nText: {text}")
            return text

    def clean_text(self, text: str) -> str:
        # Remove newlines and other special characters
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\r', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove URLs, mentions, hashtags, and special characters
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+|\#', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove emojis
        text = re.sub(r'[^\w\s,]', '', text)
        
        
        return text

    def normalize_text(self, text: str) -> str:
        # Convert text to lower case
        text = text.lower()
        # Process text with spaCy
        doc = self.nlp(text)
        # Remove stop words and lemmatize
        tokens = [token.lemma_ for token in doc if token.text not in self.stop_words and not token.is_punct]
        return ' '.join(tokens)

    def analyze_sentiment(self, text: str) -> str:
        # Clean text
        cleaned_text = self.clean_text(text)

        if len(cleaned_text) > 500:
            cleaned_text = cleaned_text[:500] 

        # Translate text to English
        translated_text = self.translate_to_english(cleaned_text)

        # Normalize text
        normalized_text = self.normalize_text(translated_text)

        # Analyze sentiment
        sentiment = self.analyzer.polarity_scores(normalized_text)
        
        return sentiment, normalized_text