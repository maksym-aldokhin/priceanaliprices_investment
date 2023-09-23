import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from random import shuffle

import negative_articles_set
import positive_articles_set
import neutral_articles_set

import csv
import os
import pickle

articles = []
labels = []
with open(os.getcwd() + '/src/training/train.csv', mode ='r', encoding='utf-8') as file:
    csvreader = csv.reader(file, delimiter = ',')
    for row in csvreader:
        if int(row[0]) == 1:
            labels.append(-1)
        else:
            labels.append(1)
        articles.append(row[2])
with open(os.getcwd() + '/src/training/test.csv', mode ='r', encoding='utf-8') as file:
    csvreader = csv.reader(file, delimiter = ',')
    for row in csvreader:
        if int(row[0]) == 1:
            labels.append(-1)
        else:
            labels.append(1)
        articles.append(row[2])


# for a in articles_dic:

# # Sample dataset (you should use your own labeled dataset)
# articles = ["This is a positive article.", "I hate this article.", "I love this article.", "Neutral article."]
# labels = [1, -1, 1, 0]  # 1 for positive, -1 for negative, 0 for neutral

# Preprocess text and extract features (TF-IDF)
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(articles)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train a logistic regression model
classifier = LogisticRegression(max_iter=10000)
classifier.fit(X_train, y_train)

# Make predictions
predictions = classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Use the model to rank new articles
new_articles = ["This is a great article.", "I dislike this article.", "It's so so"]
new_X = tfidf_vectorizer.transform(new_articles)
new_predictions = classifier.predict(new_X)

filename = os.getcwd() + '/src/models/finalized_model_amazon.sav'
pickle.dump(classifier, open(filename, 'wb'))

for article, sentiment in zip(new_articles, new_predictions):
    if sentiment == 1:
        print(f"'{article}' is positive.")
    elif sentiment == -1:
        print(f"'{article}' is negative.")
    else:
        print(f"'{article}' is neutral.")