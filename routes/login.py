from flask import Blueprint, render_template, request, redirect, url_for, flash

# Blueprint 이름을 'login'으로 만들었으니 나중에 url_for('login.login')처럼 씀
login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # DB 없이 그냥 콘솔에 출력만
        print(f"Login attempt: {username} / {password}")

        # 나중에 DB 연결하면 여기서 검증
        if username == 'admin' and password == '1234':
            flash('Login success (mock)', 'success')
            return redirect(url_for('main.home'))  # 또는 홈으로 이동
        else:
            flash('Invalid credentials (mock)', 'error')

    return render_template('login.html')
