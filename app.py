from flask import Flask, redirect,render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Knowlet

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# サインアップ
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        age = request.form.get('age')
        password = request.form.get('password')
        
        # Userのインスタンスを作成
        user = User(username=username, email=email, age=age, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    else:
        return render_template('signup.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

# ログアウト    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ホーム画面
@app.route('/', methods=['GET'])
@login_required
def index():
    if request.method == 'GET':
        # DBに登録されたデータをすべて取得する
        knowlets = Knowlet.query.all()
        return render_template('index.html', knowlets=knowlets)

# 投稿画面
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        resolved = int(request.form.get('resolved'))
        
        # Knowletのインスタンスを作成
        knowlet = Knowlet(title=title, content=content, 
                          user_id=current_user.id, resolved=resolved)
        db.session.add(knowlet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')
    
# ナレット編集画面
@app.route('/<int:knowlet_id>/edit', methods=['GET', 'POST'])
def knowlet_edit(knowlet_id):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        resolved = int(request.form.get('resolved'))
        
        # Knowletのインスタンスを作成
        knowlet = db.session.query(Knowlet).filter(Knowlet.id == knowlet_id).first() # 他にもいい書き方あるかも
        knowlet.title = title
        knowlet.content = content
        knowlet.resolved = resolved
        db.session.commit()
        return redirect('/')
    else:
        knowlet = Knowlet.query.filter(Knowlet.id == knowlet_id).first()
        return render_template('knowlet_edit.html', knowlet=knowlet)
    
# ナレット削除画面
@app.route('/<int:knowlet_id>/delete', methods=['GET', 'POST'])
def knowlet_delete(knowlet_id):
    if request.method == 'POST':
        # Knowletのインスタンスを作成
        knowlet = db.session.query(Knowlet).filter(Knowlet.id == knowlet_id).first() # 他にもいい書き方あるかも
        db.session.delete(knowlet)
        db.session.commit()
        return redirect('/')
    else:
        knowlet = Knowlet.query.filter(Knowlet.id == knowlet_id).first()
        return render_template('knowlet_delete.html', knowlet=knowlet)
        
if __name__ == "__main__":
    app.run(port=8000)