# app.py
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import re

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
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


# 首页
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        has_partner = request.form.get('has_partner')

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

        # 本人手机号校验
        if not re.fullmatch(r'\d{11}', phone):
            return '手机号必须为11位数字'

        # 本人校友卡号校验
        if not re.fullmatch(r'HUST\d{8}', card_number):
            return '校友卡号格式错误'

        # 双人报名逻辑
        if has_partner == 'yes':

            # 双人报名必须填写搭档
            if not partner_name or not partner_phone:
                return '双人报名必须填写搭档信息'

            # 搭档手机号校验
            if not re.fullmatch(r'\d{11}', partner_phone):
                return '搭档手机号必须为11位数字'

            # 搭档校友卡号校验
            if not re.fullmatch(r'HUST\d{8}', partner_card_number):
                return '搭档校友卡号格式错误'

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
            partner_card_number=partner_card_number
        )

        db.session.add(new_user)
        db.session.commit()

        return '报名成功！'

    return render_template('index.html')


# 后台页面
@app.route('/admin')
def admin():

    users = User.query.all()

    return render_template('admin.html', users=users)


# 导出Excel
@app.route('/export')
def export_excel():

    users = User.query.all()

    data = []

    for user in users:

        data.append({

            '姓名': user.name,
            '手机号': user.phone,
            '院系': user.department,
            '年级': user.grade,
            '校友卡号': user.card_number,

            '搭档姓名': user.partner_name,
            '搭档手机号': user.partner_phone,
            '搭档院系': user.partner_department,
            '搭档年级': user.partner_grade,
            '搭档校友卡号': user.partner_card_number
        })

    # 生成Excel
    df = pd.DataFrame(data)

    excel_file = '报名数据.xlsx'

    df.to_excel(excel_file, index=False)

    return send_file(excel_file, as_attachment=True)


# 启动程序
if __name__ == '__main__':

    # 创建数据库
    with app.app_context():
        db.create_all()

    app.run(debug=True)
