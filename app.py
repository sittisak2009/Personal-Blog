import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---
@app.route('/')
def home():
    posts = Post.query.all() # ดึงโพสต์ของทุกคนมาโชว์ (เหมือน Instagram Feed)
    return render_template('index.html', posts=posts)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # ตรวจสอบว่าคนลบคือเจ้าของโพสต์เท่านั้น!
    if post.user_id != current_user.id:
        flash("คุณไม่มีสิทธิ์ลบโพสต์ของคนอื่น!")
        return redirect(url_for('home'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

# (ส่วน Register/Login จะต้องทำเพิ่มในไฟล์แยกครับ)
