import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from random import shuffle

import negative_articles_set
import positive_articles_set
import neutral_articles_set

class Article:
    def __init__(self, text, rank):
        self._text = text
        self._rank = rank

    @property
    def rank(self):
        return self._rank

    @property
    def text(self):
        return self._text


unic_pos_articles = list(set(positive_articles_set.pos_articles))
unic_neg_articles = list(set(negative_articles_set.negative_articles))
unic_neu_articles = list(set(neutral_articles_set.neu_articles))

shuffle(unic_pos_articles)
shuffle(unic_neg_articles)
shuffle(unic_neu_articles)

print(len(unic_pos_articles))
print(len(unic_neg_articles))
print(len(unic_neu_articles))

unic_pos_articles = unic_pos_articles[:3000]
unic_neg_articles = unic_neg_articles[:3000]
unic_neu_articles = unic_neu_articles[:3000]

pos_articles_dic = list()
for a in unic_pos_articles:
    pos_articles_dic.append(Article(a, 1))

neg_articles_dic = list()
for a in unic_neg_articles:
    neg_articles_dic.append(Article(a, -1))

neu_articles_dic = list()
for a in unic_neu_articles:
    neu_articles_dic.append(Article(a, 0))

articles_dic = pos_articles_dic + neg_articles_dic + neu_articles_dic

shuffle(articles_dic)
print("articles_dic:", len(articles_dic))

articles = []
labels = []
for a in articles_dic:
    articles.append(a.text)
    labels.append(a.rank)

# # Sample dataset (you should use your own labeled dataset)
# articles = ["This is a positive article.", "I hate this article.", "I love this article.", "Neutral article."]
# labels = [1, -1, 1, 0]  # 1 for positive, -1 for negative, 0 for neutral

# Preprocess text and extract features (TF-IDF)
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(articles)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=100)

# Train a logistic regression model
classifier = LogisticRegression()
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

for article, sentiment in zip(new_articles, new_predictions):
    if sentiment == 1:
        print(f"'{article}' is positive.")
    elif sentiment == -1:
        print(f"'{article}' is negative.")
    else:
        print(f"'{article}' is neutral.")