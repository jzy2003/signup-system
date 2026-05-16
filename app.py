from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(100), nullable=False)

    partner_name = db.Column(db.String(100))
    partner_phone = db.Column(db.String(100))
    partner_department = db.Column(db.String(100))
    partner_grade = db.Column(db.String(100))
    partner_card_number = db.Column(db.String(100))

    has_partner = db.Column(db.String(10), nullable=False)
    dinner = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        # ======================
        # 获取数据
        # ======================
        has_partner = request.form.get('has_partner')

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

        # ======================
        # 1️⃣ 必填校验（核心）
        # ======================
        required_fields = [name, phone, department, grade, card_number, has_partner, dinner]

        if any(f is None or f.strip() == "" for f in required_fields):
            return "报名失败：所有本人信息必须填写完整"

        # ======================
        # 2️⃣ 手机号校验（11位）
        # ======================
        if not re.fullmatch(r"\d{11}", phone):
            return "报名失败：手机号必须是11位数字"

        # ======================
        # 3️⃣ 校友卡号校验（必须HUST开头 + 大写）
        # ======================
        if not re.fullmatch(r"HUST\d{8}", card_number):
            return "报名失败：校友卡号必须以大写HUST开头 + 8位数字"

        # ======================
        # 4️⃣ 搭档逻辑
        # ======================
        if has_partner == "yes":

            partner_required = [
                partner_name,
                partner_phone,
                partner_department,
                partner_grade,
                partner_card_number
            ]

            if any(f is None or f.strip() == "" for f in partner_required):
                return "报名失败：搭档信息必须填写完整"

            if not re.fullmatch(r"\d{11}", partner_phone):
                return "报名失败：搭档手机号必须是11位数字"

            if not re.fullmatch(r"HUST\d{8}", partner_card_number):
                return "报名失败：搭档校友卡号格式错误（必须HUST+8位数字）"

        else:
            partner_name = None
            partner_phone = None
            partner_department = None
            partner_grade = None
            partner_card_number = None

        # ======================
        # 5️⃣ 保存数据库
        # ======================
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

            has_partner=has_partner,
            dinner=dinner
        )

        db.session.add(new_user)
        db.session.commit()

        return "报名成功！"

    return render_template('index.html')


@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)