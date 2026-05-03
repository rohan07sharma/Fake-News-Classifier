import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib

print("Loading datasets...")
fake = pd.read_csv("Fake.csv")
real = pd.read_csv("True.csv")

fake['label'] = 0
real['label'] = 1

df = pd.concat([fake, real], axis=0).reset_index(drop=True)
df['content'] = df['title'] + " " + df['text']
df = df[['content', 'label']]

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    df['content'], df['label'], test_size=0.2, random_state=42
)

print("Vectorizing text...")
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_tfidf = tfidf.fit_transform(X_train)

print("Training model...")
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

print("Saving model and vectorizer...")
joblib.dump(model, "model.joblib")
joblib.dump(tfidf, "vectorizer.joblib")

print("Done! You can now deploy without needing the large CSV files.")
