from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (allows frontend on different ports/domains)

# Spam keywords list
SPAM_KEYWORDS = [
    'free', 'winner', 'congratulations', 'prize', 'lottery', 
    'cash', 'urgent', 'verify', 'password', 'click here',
    'million', 'dollar', 'credit card', 'limited time', 'guaranteed'
]

@app.route('/')
def home():
    return jsonify({
        "message": "Spam Detection API is running!",
        "status": "active",
        "endpoints": {
            "GET /": "API info",
            "POST /predict": "Send { 'subject': '', 'body': '' } to get spam prediction"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        subject = data.get('subject', '').lower()
        body = data.get('body', '').lower()
        
        full_text = subject + " " + body
        
        found_keywords = [kw for kw in SPAM_KEYWORDS if kw in full_text]
        spam_score = len(found_keywords)
        
        # Spam threshold: score >= 2 means spam
        is_spam = spam_score >= 2
        
        # Generate a user-friendly message
        if is_spam:
            message = f"Spam detected! Score: {spam_score}"
        else:
            message = f"Legitimate email. Score: {spam_score}"
        
        return jsonify({
            'is_spam': is_spam,
            'spam_score': spam_score,
            'found_keywords': found_keywords[:5],  # limit to first 5
            'message': message
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on all interfaces so it's accessible from other devices on the same network (if needed)
    app.run(host='0.0.0.0', port=5000, debug=True)