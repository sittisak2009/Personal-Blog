import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ข้อมูลจำลองเริ่มต้นที่มีทั้งภาพและวิดีโอ
posts = [
    {
        "id": 1,
        "title": "บรรยากาศยามเย็นริมทะเลสุดชิล",
        "date": "8 สิงหาคม 2026",
        "category": "ท่องเที่ยว",
        "content": "บันทึกความทรงจำการเดินทาง ท้องฟ้าสวย ๆ และเสียงคลื่นที่ช่วยฮีลใจในวันหยุดยาว",
        "media_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1000&auto=format&fit=crop",
        "media_type": "image"
    },
    {
        "id": 2,
        "title": "คลิปไฮไลท์ทริปขับรถเล่นรับลม",
        "date": "7 สิงหาคม 2026",
        "category": "ไลฟ์สไตล์",
        "content": "เก็บตกบรรยากาศวิวข้างทางระหว่างขับรถเดินทาง เพลงโปรดกับวิวสวย ๆ ฟินสุด ๆ",
        "media_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "media_type": "video"
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category', 'ทั่วไป')
        content = request.form.get('content')
        date = "8 สิงหาคม 2026"
        
        media_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
        media_type = "image"
        
        if 'media' in request.files:
            file = request.files['media']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                media_url = f"/{file_path}"
                
                # ตรวจสอบว่าเป็นวิดีโอหรือรูปภาพ
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in {'mp4', 'webm', 'mov'}:
                    media_type = "video"
                else:
                    media_type = "image"
        
        if title and content:
            new_post = {
                "id": len(posts) + 1 if not posts else posts[0]['id'] + 1,
                "title": title,
                "category": category,
                "date": date,
                "content": content,
                "media_url": media_url,
                "media_type": media_type
            }
            posts.insert(0, new_post)
        return redirect(url_for('home'))
        
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
        
