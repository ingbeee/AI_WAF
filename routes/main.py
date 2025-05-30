from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__)

@main.route('/')
def home():
    is_admin = session.get('role') == 'admin'
    return render_template('index.html', is_admin=is_admin)
