"""
Text preprocessing utilities
Утилиты для предварительной обработки текста
"""

import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


class TextProcessor:
    """Text preprocessing and cleaning"""
    
    def __init__(self):
        """Initialize text processor"""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words_en = set(stopwords.words('english'))
        self.stop_words_ru = set(stopwords.words('russian')) if 'russian' in stopwords.fileids() else set()
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Очистить и нормализовать текст
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags symbols but keep text
        text = re.sub(r'[@#]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters (keep letters and numbers)
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        return text
    
    def tokenize(self, text: str) -> list:
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: list, language: str = 'en') -> list:
        """Remove stopwords"""
        stop_words = self.stop_words_en if language == 'en' else self.stop_words_ru
        return [token for token in tokens if token not in stop_words]
    
    def lemmatize(self, tokens: list) -> list:
        """Lemmatize tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text: str, remove_stopwords: bool = True) -> str:
        """
        Full preprocessing pipeline
        
        Полный конвейер предварительной обработки
        """
        # Clean
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = self.lemmatize(tokens)
        
        # Join back
        return ' '.join(tokens)
