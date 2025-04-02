import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Load the training data
train_data = pd.read_csv("train.csv")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(train_data["text"], train_data["label"], test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform both the training and testing data
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Multinomial Naive Bayes classifier on the training data
model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

def train_model():
    return model
