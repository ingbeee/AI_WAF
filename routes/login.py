from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import check_password_hash

# Blueprint 이름을 'login'으로 만들었으니 나중에 url_for('login.login')처럼 씀
login = Blueprint('login', __name__)

db_config = {
    'host': 'localhost',
    'user': 'test1',
    'password': 'test1',
    'database': 'web'
}


@login.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            flash("로그인 성공!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("아이디 또는 비밀번호가 틀렸습니다.", "danger")

    return render_template('login.html')
