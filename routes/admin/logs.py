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

    return render_template('admin/logs.html')
