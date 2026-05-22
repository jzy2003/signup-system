from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据表
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


# 首页
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        name = request.form.get('name')
        phone = request.form.get('phone')
        department = request.form.get('department')
        grade = request.form.get('grade')
        card_number = request.form.get('card_number')

        partner_name = request.form.get('partner_name')
        partner_phone = request.form.get('partner_phone')
        partner_department = request.form.get('partner_department')
        partner_grade = request.form.get('partner_grade')
        partner_card_number = request.form.get('partner_card_number')

        dinner = request.form.get('dinner')

        # 手机号校验
        if not re.fullmatch(r'\d{11}', phone):
            return "手机号必须为11位数字"

        # 校友卡校验
        if not re.fullmatch(r'HUST\d{8}', card_number):
            return "校友卡号格式错误"

        # 搭档手机号校验
        if partner_phone:
            if not re.fullmatch(r'\d{11}', partner_phone):
                return "搭档手机号必须为11位数字"

        # 搭档校友卡校验
        if partner_card_number:
            if not re.fullmatch(r'HUST\d{8}', partner_card_number):
                return "搭档校友卡号格式错误"

        # 保存数据库
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

    users = User.query.all()

    return render_template('admin.html', users=users)


# 启动
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)