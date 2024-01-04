# model.py

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def train_model(X, y, use_grid_search=False):
    if use_grid_search:
        param_grid = {'alpha': [0.01, 0.1, 1, 10]}
        model = GridSearchCV(MultinomialNB(), param_grid, cv=5)
    else:
        model = MultinomialNB()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y):
    predictions = model.predict(X)
    metrics = {
        'accuracy': accuracy_score(y, predictions),
        'precision': precision_recall_fscore_support(y, predictions, average='binary')[0],
        'recall': precision_recall_fscore_support(y, predictions, average='binary')[1],
        'f1': precision_recall_fscore_support(y, predictions, average='binary')[2]
    }
    return metrics

def cross_validate_model(X, y, n_splits=10):
    model = MultinomialNB()
    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1']
    cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring)
    return cv_results