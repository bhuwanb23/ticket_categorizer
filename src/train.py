import os
import sys

# When running `python src/train.py` the interpreter sets sys.path[0] to the src/ folder.
# Ensure the project root is on sys.path so `import src.*` works reliably.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import joblib
from src.preprocess import clean_text


def load_data(path=None):
    if path is None:
        path = os.path.join(ROOT, 'data', 'tickets.csv')
    df = pd.read_csv(path)
    df = df.dropna(subset=['label'])
    n = len(df)
    subject = df['subject'].fillna('').astype(str) if 'subject' in df.columns else pd.Series([''] * n)
    body = df['body'].fillna('').astype(str) if 'body' in df.columns else pd.Series([''] * n)
    df['text'] = (subject + ' ' + body).map(clean_text)
    return df


def build_pipeline():
    # Logistic Regression gives better-calibrated probabilities than MultinomialNB
    # on this small TF-IDF setup, which makes the 60% review threshold usable.
    vect = TfidfVectorizer(min_df=1, ngram_range=(1, 2))
    clf = LogisticRegression(max_iter=2000, C=8.0)
    return vect, clf


def main():
    models_dir = os.path.join(ROOT, 'models')
    os.makedirs(models_dir, exist_ok=True)
    df = load_data()
    X = df['text'].values
    y = df['label'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )

    vect, clf = build_pipeline()
    Xtr = vect.fit_transform(X_train)
    Xte = vect.transform(X_test)
    clf.fit(Xtr, y_train)

    preds = clf.predict(Xte)
    acc = metrics.accuracy_score(y_test, preds)
    print(f"Holdout test accuracy: {acc:.3f} ({len(y_test)} samples)")
    print(metrics.classification_report(y_test, preds, zero_division=0))
    print("Confusion matrix labels:", list(clf.classes_))
    print("Confusion matrix:\n", metrics.confusion_matrix(y_test, preds, labels=clf.classes_))

    # Retrain on all labeled data before saving for inference.
    vect_full, clf_full = build_pipeline()
    X_all = vect_full.fit_transform(X)
    clf_full.fit(X_all, y)
    joblib.dump(vect_full, os.path.join(models_dir, 'vectorizer.joblib'))
    joblib.dump(clf_full, os.path.join(models_dir, 'model.joblib'))
    print(f'Saved full-data vectorizer and model to {models_dir}/')


if __name__ == '__main__':
    main()
