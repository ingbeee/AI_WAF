from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from db import db_config
from flask import session
from werkzeug.security import check_password_hash

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            session['username'] = username
            session['role'] = result[1]  # ✅ role 저장
            session.permanent = False
            flash("로그인 성공!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("아이디 또는 비밀번호가 틀렸습니다.", "danger")

    return render_template('login.html')

@login.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('main.home'))
