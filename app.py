import os
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_NAME = 'feedback.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            experience TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

def send_telegram_message(username, email, rating, experience):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("Telegram configuration is missing. Message not sent.")
        return False
        
    text = f"📝 *New Student Feedback*\n\n*Name:* {username}\n*Email:* {email}\n*Rating:* {rating}/5\n*Experience:* {experience}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send telegram message: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Exception while sending telegram message: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    
    username = data.get('username')
    email = data.get('email')
    rating = data.get('rating')
    experience = data.get('experience')
    
    if not username or not email or not rating or not experience:
        return jsonify({'error': 'All fields are required'}), 400
        
    try:
        # Save to database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO feedback (username, email, rating, experience) VALUES (?, ?, ?, ?)',
                  (username, email, rating, experience))
        conn.commit()
        conn.close()
        
        # Send Telegram notification
        send_telegram_message(username, email, rating, experience)
        
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
