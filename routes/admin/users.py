from flask import render_template, session, redirect, url_for, flash
from . import admin  # admin Blueprint
import mysql.connector
from db import db_config
from flask import request

@admin.route('/users')  # 전체 URL: /admin/users
def admin_user_list():
    if session.get('role') != 'admin':
        flash("관리자만 접근할 수 있습니다.", "error")
        return redirect(url_for('main.home'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, role, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"DB 오류: {e}", "error")
        users = []

    return render_template('admin/users.html', users=users)



@admin.route('/admin/users/<int:user_id>/update_role', methods=['POST'])
def update_role(user_id):
    if session.get('role') != 'admin':
        flash("권한이 없습니다.", "danger")
        return redirect(url_for('main.home'))

    new_role = request.form.get('role')
    if new_role not in ['admin', 'user']:
        flash("잘못된 역할입니다.", "danger")
        return redirect(url_for('admin.admin_user_list'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("역할이 변경되었습니다.", "success")
    return redirect(url_for('admin.admin_user_list'))
