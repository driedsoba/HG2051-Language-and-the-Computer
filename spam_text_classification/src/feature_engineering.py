# feature_engineering.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

def extract_features(data, vectorizer=None, max_features=1500):
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2))
        X = vectorizer.fit_transform(data['message'])
    else:
        X= vectorizer.transform(data['message'])
    y = data['label'].values
    #ros = RandomOverSampler(random_state=42)
    #X, y = ros.fit_resample(X,y)
    #rus = RandomUnderSampler(random_state=42)
    #X, y = rus.fit_resample(X, y)
    return X, y, vectorizer
