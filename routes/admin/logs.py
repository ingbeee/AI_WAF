from flask import Blueprint, render_template, session, redirect, url_for, flash
import mysql.connector
from db import db_config
from . import admin 
from flask import request

@admin.route('/logs', endpoint='admin_logs')
def admin_logs():
    if session.get('role') != 'admin':
        flash("관리자만 접근할 수 있습니다.", "danger")
        return redirect(url_for('main.home'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT idx, timestamp, ip, payload, label
        FROM logs
        WHERE ip NOT IN (SELECT ip FROM blocked_ips)
        ORDER BY timestamp DESC
        """
        cursor.execute(query)
        logs_data = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"DB 오류: {e}", "error")
        logs_data = []

    return render_template('admin/logs.html', logs=logs_data)


@admin.route('/block_ip', methods=['POST'])
def block_ip():
    ip_to_block = request.form.get('ip')
    if not ip_to_block:
        flash("차단할 IP가 없습니다.", "warning")
        return redirect(url_for('admin.admin_logs'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 중복 차단 방지
        cursor.execute("INSERT IGNORE INTO blocked_ips (ip) VALUES (%s)", (ip_to_block,))
        conn.commit()
        cursor.close()
        conn.close()
        flash(f"{ip_to_block} 차단되었습니다.", "success")
    except Exception as e:
        flash(f"차단 실패: {e}", "danger")

    return redirect(url_for('admin.admin_logs'))

@admin.route('/blocked_ips')
def blocked_ip_list():
    if session.get('role') != 'admin':
        flash("관리자만 접근할 수 있습니다.", "danger")
        return redirect(url_for('main.home'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, ip, blocked_at FROM blocked_ips ORDER BY blocked_at DESC")
        blocked_ips = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"DB 오류: {e}", "error")
        blocked_ips = []

    return render_template('admin/blocked_ips.html', blocked_ips=blocked_ips)

@admin.route('/unblock_ip/<int:ip_id>', methods=['POST'])
def unblock_ip(ip_id):
    if session.get('role') != 'admin':
        flash("권한이 없습니다.", "danger")
        return redirect(url_for('main.home'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocked_ips WHERE id = %s", (ip_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("차단된 IP가 해제되었습니다.", "success")
    except Exception as e:
        flash(f"삭제 중 오류 발생: {e}", "error")

    return redirect(url_for('admin.blocked_ip_list'))

