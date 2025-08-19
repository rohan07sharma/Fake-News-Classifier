#for data handling & visualization
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

#  converts text into numeric features.
from sklearn.feature_extraction.text import TfidfVectorizer

#  splits dataset into training & testing
from sklearn.model_selection import train_test_split

# Naive Bayes model for text classification
from sklearn.naive_bayes import MultinomialNB

# for model evaluation
from sklearn.metrics import accuracy_score, confusion_matrix

# Load datasets
fake = pd.read_csv("Fake.csv")
real = pd.read_csv("True.csv")

# Label them
fake['label'] = 0
real['label'] = 1

# Combine and reset index
df = pd.concat([fake, real], axis=0).reset_index(drop=True)

# Create content column and keep only needed cols
df['content'] = df['title'] + " " + df['text']
df = df[['content', 'label']]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df['content'], df['label'], test_size=0.2, random_state=42
)

# Vectorize text
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Predict & evaluate
y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Helper function
def predict_news(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "Real News ✅" if pred == 1 else "Fake News ❌"

# User Input Loop
while True:
    news_title = input("\nEnter news title (or type 'exit' to quit): ")
    if news_title.lower() == "exit":
        break
    result = predict_news(news_title)
    print("Prediction:", result)