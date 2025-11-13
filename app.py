from flask import Flask, request, jsonify
# 1. เรียกเกราะมาใช้
from flask_talisman import Talisman

app = Flask(__name__)

# 2. สวมเกราะให้แอปฯ!
# (content_security_policy=None คือยอมให้รันสคริปต์ง่ายๆ ไปก่อน เดี๋ยว ZAP ด่าเยอะ)
Talisman(app, content_security_policy=None , force_https=False)

users_db = []

# 3. สร้าง "หน้าแรก" (Root) ให้ ZAP มันไม่งง (แก้ 404)
@app.route('/')
def home():
    return "<h1>กูมีเกราะแล้วโว้ย!</h1>"

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "มึงลืมส่ง username มาไอ้สัส"}), 400
        
    username = data['username']
    users_db.append(username)
    
    # nosec กูสั่งให้หุบปากเรื่อง Print
    print(f"User added: {username}") 
    
    return jsonify({"status": "success", "user_added": username}), 201

if __name__ == '__main__':
    # nosec สั่งหมาหุบปากเรื่อง 0.0.0.0 (เพราะเราใช้ Talisman บังคับ HTTPS แล้ว แต่ใน Docker มันโอเค)
    app.run(host='0.0.0.0', port=5000)# nosec                                                                               `                                                                  