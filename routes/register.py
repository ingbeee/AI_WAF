from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from db import db_config
from flask import session
from werkzeug.security import generate_password_hash

register = Blueprint('register', __name__)

@register.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            # DB 연결 및 INSERT
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash("회원가입이 완료되었습니다.", "success")
            return redirect(url_for('login.login_page'))

        except mysql.connector.Error as err:
            flash(f"MySQL 오류: {err}", "danger")
            print("MySQL 예외:", err)

    return render_template('register.html')
