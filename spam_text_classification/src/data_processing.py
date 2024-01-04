# data_processing.py

import pandas as pd
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Global initialization
STOPWORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()

def load_data(file_path):
    try:
        df = pd.read_csv(file_path, sep='\t', header=None, names=['label', 'message'])
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in STOPWORDS]
    lemmatized_tokens = [LEMMATIZER.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmatized_tokens)
