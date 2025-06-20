from flask import Flask
from routes import blueprints
from flask import session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'super-secret-key-123' 
app.permanent_session_lifetime = timedelta(hours=1)

for bp in blueprints:
    app.register_blueprint(bp)

@app.context_processor
def inject_is_admin():
    return dict(is_admin=(session.get('role') == 'admin'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=4000)
