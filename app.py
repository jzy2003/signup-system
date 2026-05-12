from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re

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

    # 本人信息
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    department = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    card_number = db.Column(db.String(100))

    # 搭档信息
    partner_name = db.Column(db.String(100))
    partner_phone = db.Column(db.String(100))
    partner_department = db.Column(db.String(100))
    partner_grade = db.Column(db.String(100))
    partner_card_number = db.Column(db.String(100))

    # 晚宴
    dinner = db.Column(db.String(20))


# 首页（报名页面）
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        # 本人信息
        name = request.form.get('name')
        phone = request.form.get('phone')
        department = request.form.get('department')
        grade = request.form.get('grade')
        card_number = request.form.get('card_number')

        # 搭档信息
        partner_name = request.form.get('partner_name')
        partner_phone = request.form.get('partner_phone')
        partner_department = request.form.get('partner_department')
        partner_grade = request.form.get('partner_grade')
        partner_card_number = request.form.get('partner_card_number')

        # 晚宴
        dinner = request.form.get('dinner')

        # =========================
        # 数据格式验证
        # =========================

        # 手机号规则：11位数字
        phone_pattern = r'^\d{11}$'

        # 校友卡号规则：HUST + 8位数字
        card_pattern = r'^HUST\d{8}$'

        # 验证本人手机号
        if not re.match(phone_pattern, phone):
            return "错误：本人手机号必须是11位数字！"

        # 验证搭档手机号
        if not re.match(phone_pattern, partner_phone):
            return "错误：搭档手机号必须是11位数字！"

        # 验证本人校友卡号
        if not re.match(card_pattern, card_number):
            return "错误：本人校友卡号格式应为 HUST12345678"

        # 验证搭档校友卡号
        if not re.match(card_pattern, partner_card_number):
            return "错误：搭档校友卡号格式应为 HUST12345678"

        # =========================
        # 保存数据库
        # =========================

        new_user = User(
            name=name,
            phone=phone,
            department=department,
            grade=grade,
            card_number=card_number,

            partner_name=partner_name,
            partner_phone=partner_phone,
            partner_department=partner_department,
            partner_grade=partner_grade,
            partner_card_number=partner_card_number,

            dinner=dinner
        )

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