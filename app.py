from flask import Flask, render_template

app = Flask(__name__)

# ข้อมูลจำลองสำหรับบล็อกและแกลเลอรีของคุณ (สามารถเปลี่ยนข้อความหรือรูปภาพได้ตามใจชอบ)
posts = [
    {
        "id": 1,
        "title": "ยินดีต้อนรับสู่พื้นที่ส่วนตัวของผม",
        "date": "8 สิงหาคม 2026",
        "content": "นี่คือเว็บมินิบล็อกและไดอารี่ออนไลน์ที่ผมสร้างขึ้นด้วย Python และ Flask บันทึกเรื่องราวและประสบการณ์ต่าง ๆ ไว้ที่นี่",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
    },
    {
        "id": 2,
        "title": "รวมภาพบรรยากาศและความทรงจำ",
        "date": "7 สิงหาคม 2026",
        "content": "พื้นที่สำหรับเก็บภาพถ่ายสวย ๆ พร้อมคำบรรยายสั้น ๆ บันทึกช่วงเวลาดี ๆ ในแต่ละวัน",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1000&auto=format&fit=crop"
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
