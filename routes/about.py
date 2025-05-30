from flask import Blueprint, render_template, request, redirect, url_for, session,  flash

about = Blueprint('about', __name__)

@about.route('/about', methods=['GET', 'POST'])
def input_page():
    # 세션에 username이 없으면 홈으로 리다이렉트
    if 'username' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        flash(f"입력된 값: {user_input}", "info") 
        print(f"사용자 입력: {user_input}")
        return redirect(url_for('about.input_page'))

    return render_template('about.html')
