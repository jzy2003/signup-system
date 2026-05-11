from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# 创建 Flask 应用
app = Flask(__name__)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 创建报名数据表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))

# 首页（报名页面）
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        # 获取表单数据
        name = request.form.get('name')
        phone = request.form.get('phone')

        # 调试输出（会显示在终端）
        print("姓名：", name)
        print("电话：", phone)

        # 保存到数据库
        new_user = User(name=name, phone=phone)

        db.session.add(new_user)
        db.session.commit()

        return "报名成功！"

    return render_template('index.html')

# 后台页面
@app.route('/admin')
def admin():

    # 查询所有报名数据
    users = User.query.all()

    return render_template('admin.html', users=users)

# 启动程序
if __name__ == '__main__':

    # 自动创建数据库表
    with app.app_context():
        db.create_all()

    app.run(debug=True)