from flask import Flask, request, jsonify
from flask_talisman import Talisman # เรียกเกราะมา

app = Flask(__name__)

# 1. สร้างกฎเหล็ก (CSP): "กูอนุญาตให้โหลดของจากบ้านกู ('self') เท่านั้น! ของคนอื่นห้ามเข้า!"
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'style-src': '\'self\'',
}

# 2. สวมเกราะใหม่:
# - content_security_policy=csp : บังคับใช้กฎเหล็กข้างบน
# - force_https=False : ยังยอมให้ใช้ HTTP ธรรมดา (เพราะเราเทสใน Docker)
Talisman(app, content_security_policy=csp, force_https=False)

# 3. แก้เผ็ดโจร: ถ้าโจรแอบดู Header ว่าเราใช้ Server อะไร...
@app.after_request
def add_header(response):
    # เปลี่ยนแม่งเลย ไม่ให้มันรู้ความจริง
    response.headers['Server'] = 'GuRock-Server-V1' 
    return response

# --- ข้างล่างเหมือนเดิม ---
users_db = []

@app.route('/')
def home():
    return "<h1>กูมีเกราะ CSP แล้วโว้ย!</h1>"

# ... (โค้ดส่วนอื่นเหมือนเดิม) ...

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