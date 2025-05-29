from flask import Blueprint, render_template, request, redirect, url_for

about = Blueprint('about', __name__)

@about.route('/about', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        print(f"사용자 입력: {user_input}")
        return redirect(url_for('about.input_page'))

    return render_template('about.html')
