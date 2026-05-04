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

def check_live_news(text):
    try:
        words = [w.lower() for w in text.replace(',', '').replace('.', '').split() if len(w) > 3]
        if not words: return False, ""
        
        query = ' '.join(words[:6]) 
        q = urllib.parse.quote(query)
        url = f'https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en'
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            res = response.read()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res)
        items = root.findall('./channel/item')
        
        if not items: return False, ""
            
        # Check if the top headline contains our keywords
        top_title = items[0].find('title').text.lower()
        match_count = sum(1 for w in words[:6] if w in top_title)
        
        # If at least 2 significant words match the live headline, verify it
        if match_count >= min(2, len(words[:6])): 
            return True, items[0].find('title').text
            
    except Exception as e:
        print(f"Live verification error: {e}")
        pass
    return False, ""

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        news_text = data.get('text', '')
        if not news_text.strip():
            return jsonify({'error': 'Please enter some text to verify.'}), 400
            
        # Step 1: ML Prediction
        result = predict_news(news_text)
        is_real = "Real News" in result
        verified_headline = ""
        
        # Step 2: Live Fact-Checking for recent events
        found_live, headline = check_live_news(news_text)
        if found_live:
            is_real = True
            result = "Real News ✅"
            verified_headline = headline
            
        return jsonify({
            'prediction': result,
            'is_real': is_real,
            'verified_headline': verified_headline
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