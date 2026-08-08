import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ตั้งค่าโฟลเดอร์สำหรับเก็บรูปภาพที่อัปโหลด
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ข้อมูลจำลองเริ่มต้น
posts = [
    {
        "id": 1,
        "title": "ยินดีต้อนรับสู่พื้นที่ส่วนตัวของผม",
        "date": "8 สิงหาคม 2026",
        "content": "นี่คือเว็บมินิบล็อกและแกลเลอรีที่อัปเกรดใหม่ สามารถอัปโหลดรูปภาพจากเครื่องและลบโพสต์ได้แล้ว!",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = "8 สิงหาคม 2026"
        
        # จัดการไฟล์รูปภาพที่อัปโหลด
        image_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1000&auto=format&fit=crop" # รูปสำรอง
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f"/{file_path}" # บันทึก path สำหรับเรียกใช้งานบนเว็บ
        
        if title and content:
            new_post = {
                "id": len(posts) + 1 if not posts else posts[0]['id'] + 1,
                "title": title,
                "date": date,
                "content": content,
                "image": image_url
            }
            posts.insert(0, new_post)
        return redirect(url_for('home'))
        
    return render_template('add.html')

# เส้นทางสำหรับลบโพสต์
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    
