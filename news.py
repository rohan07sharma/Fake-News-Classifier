import joblib
from flask import Flask, render_template, request, jsonify
import traceback

print("Loading saved model and vectorizer...")
try:
    model = joblib.load("model.joblib")
    tfidf = joblib.load("vectorizer.joblib")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please run `python train_model.py` first to generate the models.")
    # Exiting or continuing without model will fail later, but for now we just print


# Helper function
def predict_news(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "Real News ✅" if pred == 1 else "Fake News ❌"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        news_text = data.get('text', '')
        if not news_text.strip():
            return jsonify({'error': 'Please enter some text to verify.'}), 400
            
        result = predict_news(news_text)
        is_real = "Real News" in result
        
        return jsonify({
            'prediction': result,
            'is_real': is_real
        })
    except Exception as e:
        print(f"Error during prediction: {traceback.format_exc()}")
        return jsonify({'error': 'An error occurred during prediction.'}), 500

import urllib.request
import xml.etree.ElementTree as ET

@app.route('/fetch_live_news', methods=['GET'])
def fetch_live_news():
    try:
        # Fetch news from a public RSS feed (e.g., BBC News)
        url = 'http://feeds.bbci.co.uk/news/rss.xml'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        news_list = []
        
        # Get the first 5 news items
        for item in root.findall('./channel/item')[:5]:
            title = item.find('title').text if item.find('title') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            if title and description:
                news_list.append({
                    'title': title,
                    'text': title + ". " + description # Combine title and description for better context
                })
                
        return jsonify({'news': news_list})
    except Exception as e:
        print(f"Error fetching live news: {e}")
        return jsonify({'error': 'Could not fetch live news at this time.'}), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, use_reloader=False)