from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load and prepare the dataset
df = pd.read_csv("Cleaned_Split_Ecommerce_dataset.csv")
queries = df['query'].fillna("")
responses = df['response'].fillna("")

# Vectorize the queries
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(queries)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({'reply': "Please enter a valid message."})

    # Vectorize the user message
    user_vector = vectorizer.transform([user_message])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_vector, X)
    best_match_index = np.argmax(similarity_scores)

    # Apply a threshold to determine if a good match exists
    if similarity_scores[0, best_match_index] > 0.4:
        reply = responses[best_match_index]
    else:
        reply = "Sorry, I couldn't find a suitable response."

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)
