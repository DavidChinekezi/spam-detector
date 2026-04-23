from flask import Flask, request, jsonify

app = Flask(__name__)

# Spam keywords list
SPAM_KEYWORDS = ['free', 'winner', 'congratulations', 'prize', 'lottery', 
                 'cash', 'urgent', 'verify', 'password', 'click here']

@app.route('/')
def home():
    return jsonify({"message": "Spam Detection API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    subject = data.get('subject', '').lower()
    body = data.get('body', '').lower()
    
    full_text = subject + " " + body
    
    found_keywords = [kw for kw in SPAM_KEYWORDS if kw in full_text]
    spam_score = len(found_keywords)
    
    is_spam = spam_score >= 2
    
    return jsonify({
        'is_spam': is_spam,
        'spam_score': spam_score,
        'found_keywords': found_keywords[:5],
        'message': 'Spam detected!' if is_spam else 'Legitimate email'
    })

if __name__ == '__main__':
    app.run(debug=True)