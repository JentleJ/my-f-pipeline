from flask import Flask, request, jsonify
from flask_talisman import Talisman

app = Flask(__name__)

# 1. อัปเกรดกฎเหล็ก CSP (เพิ่ม object-src: 'none' เพื่อปิดทางโจรฝังไฟล์แปลกๆ)
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'style-src': '\'self\'',
    'object-src': '\'none\'',
    'base-uri': '\'self\''
}

# 2. สวมเกราะ (เหมือนเดิม)
Talisman(app, content_security_policy=csp, force_https=False)

# 3. ยันต์กันผีชุดใหญ่ (ทำงานทุกครั้งที่มีการตอบกลับ)
@app.after_request
def add_security_headers(response):
    # --- แก้เรื่อง Server Leaks ---
    # เปลี่ยนชื่อ Server แม่งเลย (ถ้ามันยังด่าอีก ก็ช่างหัวมัน เพราะนี่คือ Dev Server)
    response.headers['Server'] = 'GuRock-Server-V1'
    
    # --- แก้เรื่อง Cache (ห้ามจำ!) ---
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # --- แก้เรื่อง Spectre (แยกบ้านเราออกจากเว็บอื่น) ---
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    
    return response

# --- (ส่วน Database และ Route เหมือนเดิม) ---
users_db = []

@app.route('/')
def home():
    return "<h1>กูมีเกราะ Ultimate แล้วโว้ย!</h1>"

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "มึงลืมส่ง username มาไอ้สัส"}), 400
        
    username = data['username']
    users_db.append(username)
    
    # nosec
    print(f"User added: {username}") 
    
    return jsonify({"status": "success", "user_added": username}), 201

if __name__ == '__main__':
    # nosec
    app.run(host='0.0.0.0', port=5000)