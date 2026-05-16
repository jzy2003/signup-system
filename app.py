from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

# 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 数据表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 本人
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    department = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    card_number = db.Column(db.String(100))

    # 搭档
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

        has_partner = request.form.get('has_partner')

        # 本人
        name = request.form.get('name')
        phone = request.form.get('phone')
        department = request.form.get('department')
        grade = request.form.get('grade')
        card_number = request.form.get('card_number')

        # 搭档
        partner_name = request.form.get('partner_name')
        partner_phone = request.form.get('partner_phone')
        partner_department = request.form.get('partner_department')
        partner_grade = request.form.get('partner_grade')
        partner_card_number = request.form.get('partner_card_number')

        dinner = request.form.get('dinner')

        # ====== 校验规则 ======
        phone_pattern = r'^\d{11}$'
        card_pattern = r'^HUST\d{8}$'

        # 本人校验
        if not re.match(phone_pattern, phone):
            return "错误：手机号必须是11位数字！"

        if not re.match(card_pattern, card_number):
            return "错误：校友卡号必须是 HUST + 8位数字"

        # 双人报名才校验搭档
        if has_partner == 'yes':

            if not re.match(phone_pattern, partner_phone):
                return "错误：搭档手机号必须是11位数字！"

            if not re.match(card_pattern, partner_card_number):
                return "错误：搭档校友卡号必须是 HUST + 8位数字"

        else:
            partner_name = None
            partner_phone = None
            partner_department = None
            partner_grade = None
            partner_card_number = None

        # 保存
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