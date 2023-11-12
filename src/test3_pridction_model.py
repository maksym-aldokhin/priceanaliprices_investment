import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

# Define preprocessing function
def preprocess_text(text):
    # Tokenization
    words = word_tokenize(text)

    # Stopword removal
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    return ' '.join(words)

import negative_articles_set
import positive_articles_set
import neutral_articles_set

positive_dataset = list(set(positive_articles_set.pos_articles))
negative_dataset = list(set(negative_articles_set.negative_articles))
neutral_dataset = list(set(neutral_articles_set.neu_articles))

# Preprocess your datasets
positive_data = [preprocess_text(text) for text in positive_dataset]
negative_data = [preprocess_text(text) for text in negative_dataset]
neutral_data = [preprocess_text(text) for text in neutral_dataset]

from sklearn.feature_extraction.text import TfidfVectorizer

# Combine all data and labels
all_data = positive_data + negative_data + neutral_data
labels = ['positive'] * len(positive_data) + ['negative'] * len(negative_data) + ['neutral'] * len(neutral_data)

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(all_data)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

from sklearn.metrics import accuracy_score

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

def predict_sentiment(text):
    preprocessed_text = preprocess_text(text)
    text_vectorized = tfidf_vectorizer.transform([preprocessed_text])
    prediction = model.predict(text_vectorized)
    return prediction[0]

# Example usage
real_data = "This movie was great! I loved the plot and the characters."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "MacBook Pro images demonstrates reason for battery recall"
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "Photos have been shared of a designer's Mid-2015 15-inch Retina MacBook Pro that has suffered a catastrophic battery failure, images that illustrate why Apple recently instigated a recall program for some units of that particular model. On June 20, Apple launched a voluntary recall of the 15-inch MacBook Pro, specifically those sold between September 2015 and February 2017, over concerns the battery posed a safety risk. Under the recall, which provides a replacement battery for affected Mac notebooks, Apple explained the battery \"may overheat and pose a fire safety risk\" in some cases, something that has been illustrated by one unlucky owner. Designer Steven Gagne of Pensacola, Florida, encountered a failure of his MacBook Pro's battery on June 17 while in bed, according to a Facebook post spotted by PetaPixel. The battery \"blew and a small fire filled my house with smoke,\" wrote Gagne, noting the sound of the event and the strong chemical and burning smell. One concern was that the MacBook Pro wasn't actively being used by Gagne at the time of the incident. He claims it was sitting \"screen closed, unplugged, and in Sleep Mode\" on a coffee table. Gagne was lucky in that normally the MacBook Pro was kept in a basket filled with notebooks and journals, or on the couch, with either location potentially causing far more damage than what transpired."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "Apple: We'll Fix the 2019 iPad Air's Blank Screen"
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "Apple is extending its repair program to the iPad Air (2019) and its blank screen issue. Some customers report their units' displays flicker before going blank permanently, so the Cupertino-based company will repair affected units free of charge. Apple didn't explain what causes the issue, but there's likely a manufacturing fault behind the LCD panel that disables functionality. Software-side issues are normally fixed through over-the-air updates. As it relates to hardware, Apple needs to intervene and manually fix the tablet.\"Apple has determined that, under certain circumstances, the screen on a limited number of iPad Air (3rd generation) devices may go blank permanently,\" the company says on its support page. \"A brief flicker or flash may appear before the screen goes blank.\" Eligible units were manufactured between March 2019 and October 2019. Since that period includes the iPad Air's release date last spring, there could be a significant amount of affected units. Yet it's up to customers to identify the issue and put in a claim that sees their units repaired under the terms of Apple's program. You'll need to get in touch with Apple or an Apple Authorized Service Provider within two years of the unit's first retail sale. It didn't specify an expiration date for the repair program, but Apple doesn't want to continue dealing with broken iPad Air (2019) units for a very long time. Plus, there's no reason to wait. Apple isn't charging a fee to fix the issue, and you'll receive a fully functioning iPad Air afterward."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "APPLE BITE Millions of iPhone users warned of horrifying new danger – check your device now"
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "The latest discovery allows hackers to bypass security protections to inject malware onto the iPhone or iPad. This malicious code grants fraudsters access to that device's photo and video album, messages, address book and calendar. It means cyber criminals could potentially spy on users using their devices audio and video capabilities. However, there is a really simple way to protect yourself."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "Three things to know if you're going to upgrade to iPhone 15"
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "CNN's senior tech writer Samantha Kelly got a hands on look at Apple's new iPhone 15 and says these are the three major changes you should know about it."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "Philadelphia is too often in crisis mode, which does nothing to stop future crises"
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)

real_data = "If we care about people hundreds of miles away, we ought to care about people hundreds of years away. It’s a simple idea that can have an outsized influence on how we set and shape policy. Many Philadelphians confront life-threatening challenges — gun violence, poverty, housing, addiction — that need to be addressed urgently. Yet lasting change is a generations-long project. The most effective way to balance this is to radically extend the timeline on which we debate and implement priorities. In other cities and countries, this message is coming across clearly. Wales, for instance, adopted the Well-being of Future Generations Act in 2015, which forces lawmakers to consider the long-term impact of their decisions. Long-term thinking is about balance. Our city’s big problems easily attract crisis thinking, in which city leaders (both public and private) often respond reactively. As a consequence, we remain mired in “servicing poverty” — or barely addressing basic needs without addressing the root causes."
predicted_sentiment = predict_sentiment(real_data)
print("Predicted sentiment:", predicted_sentiment)