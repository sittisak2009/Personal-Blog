from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# เก็บข้อมูลโพสต์ไว้ใน List (ข้อมูลจะรีเซ็ตเมื่อ Restart เซิร์ฟเวอร์บน Render)
posts = [
    {
        "id": 1,
        "title": "ยินดีต้อนรับสู่พื้นที่ส่วนตัวของผม",
        "date": "8 สิงหาคม 2026",
        "content": "นี่คือเว็บมินิบล็อกและไดอารี่ออนไลน์ที่ผมสร้างขึ้นด้วย Python และ Flask บันทึกเรื่องราวและประสบการณ์ต่าง ๆ ไว้ที่นี่",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

# หน้าสำหรับกดเพิ่มโพสต์ใหม่
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.form.get('image')
        date = "8 สิงหาคม 2026" # หรือใช้วันที่ปัจจุบัน
        
        if title and content:
            new_post = {
                "id": len(posts) + 1,
                "title": title,
                "date": date,
                "content": content,
                "image": image if image else "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1000&auto=format&fit=crop"
            }
            posts.insert(0, new_post) # เอาอันใหม่ไว้บนสุด
        return redirect(url_for('home'))
        
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
            
