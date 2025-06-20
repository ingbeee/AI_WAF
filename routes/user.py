from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import mysql.connector
from db import db_config  # DB 설정 모듈
import re

user = Blueprint('user', __name__, url_prefix='/user')

def simple_filter(s: str) -> str:
    # 1) HTML 태그 꺾쇠 이스케이프
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    # 2) script, select 제거 (대소문자 무시)
    s = re.sub(r'(?i)script', '', s)
    s = re.sub(r'(?i)select', '', s)
    return s

@user.route('/find', methods=['GET'])
def find_user():
    if 'username' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('main.home'))

    raw_input = request.args.get('user_query', '')
    filtered_input = simple_filter(raw_input)
    users = []

    if raw_input:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id, username, role, created_at 
                FROM users 
                WHERE username LIKE %s AND role != 'admin'
            """
            cursor.execute(query, (f"%{filtered_input}%",))
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            flash(f"DB 오류: {e}", "error")
            users = []

        flash(f"입력된 값: {filtered_input}", "info")
        print(f"원본: {raw_input}")
        print(f"필터 후: {filtered_input}")

    return render_template('find.html', users=users)
