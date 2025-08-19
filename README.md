# 📰 Fake News Classifier

A Machine Learning project that classifies news articles as **Real** or **Fake** using Natural Language Processing (NLP) and the Multinomial Naive Bayes algorithm.

---

## 📂 Dataset Instructions
⚠️ **Note:** The dataset is not included in this repository (files are larger than GitHub’s 25 MB limit).  

To run this project:  
1. Download the **Fake and Real News Dataset** (for example: [Kaggle Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset) or any other similar dataset).  
2. Place the dataset files in the **same folder** as `news.py`.  
3. Rename the files exactly as:  
   - `Fake.csv` → contains fake news articles  
   - `True.csv` → contains real news articles  

Your folder should look like this:
```
Fake-News-Classifier/
├── news.py
├── Fake.csv
├── True.csv
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/Fake-News-Classifier.git
   cd Fake-News-Classifier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python news.py
   ```

4. After training, the program will ask you to type some **keywords or short text** in the terminal.  
   - Example:  
     ```
     Input: "Donald Trump wins election"
     Output: True (Real News)
     ```  
     ```
     Input: "Aliens attacked New York"
     Output: Fake (Fake News)
     ```

---

## 📊 Results
- Model: **Multinomial Naive Bayes**
- Accuracy: ~92% (update with your result)
- Confusion Matrix & plots included in code.

---

## 📌 Future Improvements
- Try advanced models (Logistic Regression, Random Forest, LSTMs, Transformers).
- Deploy as a web app with Streamlit/Flask.

---

## 👨‍💻 Author
- **Rohan Sharma**
- [LinkedIn](https://linkedin.com) | [GitHub](https://github.com)
