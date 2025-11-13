
from flask import Flask, request, jsonify

# 1. สร้าง "พิมพ์เขียว" ของบ้าน
app = Flask(__name__)

# 2. แกล้งทำเป็นมี "ตู้เก็บของ" (Database)
users_db = []

# 3. สร้าง "ประตูบ้าน"
#    (รับเฉพาะ 'POST', ที่อยู่คือ '/api/v1/users')
@app.route('/api/v1/users', methods=['POST'])
def add_user():
    
    # 4. "คนเฝ้าประตู" จะเช็กของที่ส่งมา
    data = request.get_json()

    # 5. ถ้ามันไม่มี 'username' มา... ด่ามันกลับไป
    if not data or 'username' not in data:
        return jsonify({"error": "มึงลืมส่ง username มาไอ้สัส"}), 400
        
    # 6. ถ้ามี... ก็เอาของ (username) ไปเก็บ
    username_from_user = data['username']
    users_db.append(username_from_user)
    
    print(f"มีคนเพิ่ม user: {username_from_user}")
    print(f"ในตู้ตอนนี้มี: {users_db}")

    # 7. บอกมันว่า "เก็บของให้แล้วนะ"
    return jsonify({"status": "success", "user_added": username_from_user}), 201
    
# 8. คำสั่ง "เปิดบ้าน" (รันเซิร์ฟเวอร์)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #nosec