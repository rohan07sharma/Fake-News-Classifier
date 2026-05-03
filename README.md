# 🔍 Fake News Classifier (Full-Stack Web App)

A modern, full-stack Machine Learning web application that classifies news articles as **Real** or **Fake** using Natural Language Processing (NLP) and the Multinomial Naive Bayes algorithm. 

This project has evolved from a simple Python script into a fully deployable web application with a beautiful UI, real-time news fetching, and optimized model loading!

---

## ✨ Features
- **Modern Web Interface:** A sleek, glassmorphism-styled frontend built with HTML, CSS, and JavaScript.
- **Real-Time News Fetching:** Instantly fetches the latest real-world news from the BBC RSS feed for live testing.
- **Optimized Backend:** Uses a pre-trained `joblib` model to ensure the Flask server boots up instantly and uses minimal RAM (deployment-ready!).
- **High Accuracy:** Powered by TF-IDF Vectorization and a Multinomial Naive Bayes model.

---

## 📂 Project Structure
```text
Fake-News-Classifier/
├── news.py                 # The main Flask backend server
├── train_model.py          # Script to re-train and generate the model/vectorizer
├── model.joblib            # Pre-trained Naive Bayes model
├── vectorizer.joblib       # Pre-trained TF-IDF vectorizer
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignores large datasets and virtual environments
├── static/
│   ├── style.css           # Modern CSS styling
│   └── script.js           # Frontend logic and API calls
└── templates/
    └── index.html          # Main HTML structure
```

*(Note: The `Fake.csv` and `True.csv` datasets are required only if you want to re-train the model, and are ignored by Git due to their size).*

---

## 🚀 How to Run Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/<your-username>/Fake-News-Classifier.git
   cd Fake-News-Classifier
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server:**
   ```bash
   python news.py
   ```

4. **Open your browser:**
   Navigate to `http://127.0.0.1:5000` to interact with the web app!

---

## 🔧 How to Re-train the Model (Optional)
If you want to update the model with new data:
1. Download the **Fake and Real News Dataset** (e.g., from Kaggle).
2. Place `Fake.csv` and `True.csv` in the root folder.
3. Run `python train_model.py` to generate new `.joblib` files.

---

## 🌐 Deployment Ready
This project is fully configured to be deployed on platforms like **Render** or **Heroku**:
- Uses `gunicorn` for the production web server.
- Bypasses dataset loading on boot by relying on the optimized `joblib` files to prevent memory timeouts.

---

## 👨‍💻 Author
- **Rohan Sharma**
- [LinkedIn](https://linkedin.com) | [GitHub](https://github.com)
