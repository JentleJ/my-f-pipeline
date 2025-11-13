FROM python:3.10-slim

WORKDIR /app

# ก๊อปไฟล์รายการของมาก่อน
COPY requirements.txt .
# ลงของตามรายการ (Flask + Talisman)
RUN pip install -r requirements.txt

# ค่อยก๊อปโค้ดที่เหลือ
COPY . .

CMD ["python", "app.py"]