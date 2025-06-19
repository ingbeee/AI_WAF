from flask import Blueprint, render_template, session, redirect, url_for, flash
import mysql.connector
from db import db_config
from . import admin 
from flask import request

@admin.route('/logs')
def admin_logs():
    if session.get('role') != 'admin':
        flash("관리자만 접근할 수 있습니다.", "danger")
        return redirect(url_for('main.home'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idx, timestamp, ip, payload, label FROM logs ORDER BY timestamp DESC")
        logs_data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"DB 오류: {e}", "error")
        logs_data = []

    return render_template('admin/logs.html', logs=logs_data)
