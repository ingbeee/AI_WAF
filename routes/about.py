import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

about = Blueprint('about', __name__)

def simple_filter(s: str) -> str:
    # 1) HTML 태그 꺾쇠는 이스케이프
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    # 2) 'script' 키워드 제거 (대소문자 무시)
    s = re.sub(r'(?i)script', '', s)
    # 3) 'select' 키워드 제거 (대소문자 무시)
    s = re.sub(r'(?i)select', '', s)
    return s

@about.route('/about', methods=['GET', 'POST'])
def input_page():
    if 'username' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        raw = request.form.get('user_input', '')
        safe = simple_filter(raw)

        flash(f"입력된 값: {safe}", "info")
        print(f"원본: {raw}")
        print(f"필터 후: {safe}")
        return redirect(url_for('about.input_page'))

    return render_template('about.html')
