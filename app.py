from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    department = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    card_number = db.Column(db.String(100))

    partner_name = db.Column(db.String(100))
    partner_phone = db.Column(db.String(100))
    partner_department = db.Column(db.String(100))
    partner_grade = db.Column(db.String(100))
    partner_card_number = db.Column(db.String(100))

    has_partner = db.Column(db.String(10))
    dinner = db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        errors = []   # ⭐ 所有错误收集在这里

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
        # 1️⃣ 必填检测
        # ======================
        if not all([name, phone, department, grade, card_number, has_partner, dinner]):
            errors.append("本人信息存在未填写项")

        # ======================
        # 2️⃣ 手机号检测
        # ======================
        if phone and not re.fullmatch(r"\d{11}", phone):
            errors.append("本人手机号必须是11位数字")

        # ======================
        # 3️⃣ 校友卡检测（大写HUST）
        # ======================
        if card_number and not re.fullmatch(r"HUST\d{8}", card_number):
           errors.append("校友卡填写错误")

        # ======================
        # 4️⃣ 搭档检测
        # ======================
        if has_partner == "yes":

            if not all([partner_name, partner_phone, partner_department, partner_grade, partner_card_number]):
                errors.append("搭档信息存在未填写项")

            if partner_phone and not re.fullmatch(r"\d{11}", partner_phone):
                errors.append("搭档手机号必须是11位数字")

            if partner_card_number and not re.fullmatch(r"HUST\d{8}", partner_card_number):
                errors.append("校友卡填写错误")

        # ======================
        # 5️⃣ 如果有错误 → 一次性返回
        # ======================
        if errors:
            return "<br>".join(errors)

        # ======================
        # 6️⃣ 保存数据
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)